from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app import db
import requests
import json
import os
import time  

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/')
def index():
    """设置页面"""
    # 从配置文件或数据库加载设置
    try:
        with open('app/config/ai_settings.json', 'r') as f:
            ai_settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        ai_settings = {
            'model': 'gpt-3.5-turbo',
            'api_key': '',
            'api_base_url': 'https://api.openai.com/v1',
            'temperature': 0.7,
            'max_tokens': 2000
        }
    
    return render_template('settings.html', ai_settings=ai_settings)

@settings_bp.route('/save', methods=['POST'])
def save_settings():
    """保存设置"""
    model = request.form.get('model')
    api_key = request.form.get('api_key')
    api_base_url = request.form.get('api_base_url')
    temperature = float(request.form.get('temperature', 0.7))
    max_tokens = int(request.form.get('max_tokens', 2000))
    
    # 保存设置到配置文件
    ai_settings = {
        'model': model,
        'api_key': api_key,
        'api_base_url': api_base_url,
        'temperature': temperature,
        'max_tokens': max_tokens
    }
    
    # 确保目录存在
    os.makedirs('app/config', exist_ok=True)
    
    with open('app/config/ai_settings.json', 'w') as f:
        json.dump(ai_settings, f, indent=4)
    
    flash('设置已保存', 'success')
    return redirect(url_for('settings.index'))

@settings_bp.route('/generate_ai_words', methods=['POST'])
def generate_ai_words():
    """根据主题生成单词列表"""
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        
        if not topic:
            return jsonify({'success': False, 'error': '请提供有效的主题'})
        
        # 加载 AI 设置
        try:
            with open('app/config/ai_settings.json', 'r') as f:
                ai_settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({'success': False, 'error': '未找到 AI 设置，请先完成设置'})
        
        api_key = ai_settings.get('api_key')
        if not api_key:
            return jsonify({'success': False, 'error': '未设置 API 密钥，请在设置页面配置'})
        
        # 构建 AI 请求
        prompt = f"""你是一个根据用户的需求专业的英文单词提供者（如果用户没有指定需要多少单词，默认50词）。你提供的格式如下，

参考格式：

1. Malignant - 恶性的
2. Benign - 良性的
3. Biopsy - 活检
4. Oncology - 肿瘤学
5. Metastasis - 转移

用户需求: {topic}

你作为一个ai你的回答，只能输出参考格式的内容，不能输出任何无关的字符，要确保输出格式和参考格式一致。"""

        # 请求头和负载
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        payload = {
            'model': ai_settings.get('model', 'gpt-3.5-turbo'),
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': ai_settings.get('temperature', 0.7),
            'max_tokens': ai_settings.get('max_tokens', 2000)
        }
        
        api_base_url = ai_settings.get('api_base_url', 'https://api.openai.com/v1')
        
        # 添加重试机制
        max_retries = 3
        current_retry = 0
        timeout = 60  # 增加到60秒
        
        while current_retry < max_retries:
            try:
                print(f"正在尝试请求 AI API (尝试 {current_retry+1}/{max_retries})...")
                
                # 发起请求并增加超时时间
                response = requests.post(
                    f"{api_base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=timeout
                )
                
                if response.status_code != 200:
                    error_info = response.json().get('error', {}).get('message', '未知错误')
                    print(f"API错误: {error_info}")
                    if "rate limit" in error_info.lower():
                        # 如果是速率限制错误，重试并增加延迟
                        current_retry += 1
                        if current_retry < max_retries:
                            time.sleep(2 * current_retry)  # 逐渐增加延迟
                            continue
                    return jsonify({'success': False, 'error': f'API 错误: {error_info}'})
                
                result = response.json()
                words_content = result['choices'][0]['message']['content'].strip()
                
                return jsonify({'success': True, 'words': words_content})
            
            except requests.exceptions.Timeout:
                current_retry += 1
                print(f"请求超时 - 重试 {current_retry}/{max_retries}")
                if current_retry >= max_retries:
                    return jsonify({'success': False, 'error': f'请求超时(尝试了{max_retries}次)。请检查网络连接或API服务器状态。'})
                # 指数退避策略增加重试时间间隔
                time.sleep(2 * current_retry)
            
            except requests.exceptions.ConnectionError:
                return jsonify({'success': False, 'error': '连接错误，无法连接到API服务器。请检查API地址是否正确。'})
            
            except Exception as e:
                print(f"请求过程中发生错误: {str(e)}")
                return jsonify({'success': False, 'error': f'请求出错: {str(e)}'})
        
    except Exception as e:
        print(f"生成单词过程中发生错误: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})