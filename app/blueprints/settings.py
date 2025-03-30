from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app import db
import requests
import json
import os
import time  
from flask import jsonify, request, current_app
from webdav3.client import Client
import datetime  
import shutil  # 添加这一行

settings_bp = Blueprint('settings', __name__)

# 在index函数中添加WebDAV设置传递
@settings_bp.route('/')
def index():
    """设置页面"""
    # 获取AI设置和WebDAV设置
    ai_settings = get_ai_settings()
    webdav_settings = get_webdav_settings()
    
    return render_template('settings.html', 
                          ai_settings=ai_settings,
                          webdav_settings=webdav_settings)

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
    




# 添加获取WebDAV设置的辅助函数
def get_webdav_settings():
    """获取WebDAV设置"""
    settings_file = os.path.join('app', 'config', 'webdav_settings.json')
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            return json.load(f)
    return None


# 获取AI设置的辅助函数
def get_ai_settings():
    """获取AI设置"""
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
    return ai_settings




# 本地备份路由
@settings_bp.route('/create_backup', methods=['POST'])
def create_backup():
    """创建本地数据库备份"""
    try:
        # 数据库路径
        db_path = os.path.join('app', 'wordweb.db')
        
        # 确保数据库文件存在
        if not os.path.exists(db_path):
            return jsonify({'success': False, 'error': '数据库文件不存在'})
        
        # 创建带有时间戳的备份文件名
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join('app', f'wordweb_{timestamp}.db.bak')
        
        # 复制数据库文件
        shutil.copy2(db_path, backup_path)
        
        return jsonify({
            'success': True, 
            'backup_path': backup_path,
            'message': f'备份已创建: {backup_path}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# WebDAV验证路由
@settings_bp.route('/verify_webdav', methods=['POST'])
def verify_webdav():
    """验证WebDAV连接"""
    try:
        data = request.json
        url = data.get('url')
        username = data.get('username')
        password = data.get('password')
        
        # 如果密码是掩码，则从存储的WebDAV设置中获取真实密码
        if password == '••••••••':
            stored_settings = get_webdav_settings()
            if stored_settings and 'password' in stored_settings:
                password = stored_settings['password']
        
        if not url or not username or not password:
            return jsonify({'success': False, 'error': '请提供完整的WebDAV信息'})
        
        # 确保url以/结束
        if not url.endswith('/'):
            url += '/'
        
        # 配置WebDAV客户端
        options = {
            'webdav_hostname': url,
            'webdav_login': username,
            'webdav_password': password,
            'webdav_timeout': 30
        }
        
        client = Client(options)
        
        # 检查连接是否成功
        if client.check():
            # 尝试创建wordweb目录(如果不存在)
            try:
                if not client.check('wordweb'):
                    client.mkdir('wordweb')
            except:
                # 如果创建目录失败，可能已经存在或权限不足
                pass
                
            return jsonify({'success': True, 'message': 'WebDAV连接成功'})
        else:
            return jsonify({'success': False, 'error': 'WebDAV连接失败'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'WebDAV连接错误: {str(e)}'})
# 保存WebDAV设置
@settings_bp.route('/save_webdav', methods=['POST'])
def save_webdav():
    """保存WebDAV设置"""
    try:
        data = request.json
        url = data.get('url')
        username = data.get('username')
        password = data.get('password')
        
        if not url or not username or not password:
            return jsonify({'success': False, 'error': '请提供完整的WebDAV信息'})
        
        # 确保url以/结束
        if not url.endswith('/'):
            url += '/'
        
        # 创建设置对象
        webdav_settings = {
            'url': url,
            'username': username,
            'password': password
        }
        
        # 确保目录存在
        os.makedirs('app/config', exist_ok=True)
        
        # 保存设置
        with open('app/config/webdav_settings.json', 'w') as f:
            json.dump(webdav_settings, f, indent=4)
        
        return jsonify({'success': True, 'message': 'WebDAV设置已保存'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# 上传数据库到WebDAV
@settings_bp.route('/upload_db', methods=['POST'])
def upload_db():
    """上传数据库到WebDAV服务器"""
    try:
        # 获取WebDAV设置
        webdav_settings = get_webdav_settings()
        if not webdav_settings:
            return jsonify({'success': False, 'error': 'WebDAV设置不存在'})
        
        # 数据库路径
        db_path = os.path.join('app', 'wordweb.db')
        
        # 确保数据库文件存在
        if not os.path.exists(db_path):
            return jsonify({'success': False, 'error': '数据库文件不存在'})
        
        # 配置WebDAV客户端
        options = {
            'webdav_hostname': webdav_settings['url'],
            'webdav_login': webdav_settings['username'],
            'webdav_password': webdav_settings['password'],
            'webdav_timeout': 30
        }
        
        client = Client(options)
        
        # 确保目标目录存在
        try:
            if not client.check('wordweb'):
                client.mkdir('wordweb')
        except:
            # 如果创建目录失败，目录可能已存在
            pass
        
        # 上传数据库文件
        remote_path = 'wordweb/wordweb.db'
        client.upload_sync(remote_path=remote_path, local_path=db_path)
        
        # 添加上传时间戳文件
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp_file = os.path.join('app', 'last_upload.txt')
        
        with open(timestamp_file, 'w') as f:
            f.write(f'最后上传时间: {timestamp}')
        
        try:
            client.upload_sync(remote_path='wordweb/last_upload.txt', local_path=timestamp_file)
            os.remove(timestamp_file)  # 清理临时文件
        except:
            # 时间戳文件上传失败不影响主功能
            pass
        
        return jsonify({'success': True, 'message': '数据库上传成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# 从WebDAV下载数据库
@settings_bp.route('/download_db', methods=['POST'])
def download_db():
    """从WebDAV服务器下载数据库"""
    try:
        # 获取WebDAV设置
        webdav_settings = get_webdav_settings()
        if not webdav_settings:
            return jsonify({'success': False, 'error': 'WebDAV设置不存在'})
        
        # 数据库路径
        db_path = os.path.join('app', 'wordweb.db')
        
        # 先创建本地备份
        backup_timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join('app', f'wordweb_before_download_{backup_timestamp}.db.bak')
        
        # 如果本地数据库存在，先备份
        if os.path.exists(db_path):
            shutil.copy2(db_path, backup_path)
        
        # 配置WebDAV客户端
        options = {
            'webdav_hostname': webdav_settings['url'],
            'webdav_login': webdav_settings['username'],
            'webdav_password': webdav_settings['password'],
            'webdav_timeout': 30
        }
        
        client = Client(options)
        
        # 检查远程文件是否存在
        remote_path = 'wordweb/wordweb.db'
        if not client.check(remote_path):
            return jsonify({'success': False, 'error': '服务器上不存在数据库文件'})
        
        # 下载数据库文件
        client.download_sync(remote_path=remote_path, local_path=db_path)
        
        return jsonify({
            'success': True, 
            'message': '数据库下载成功',
            'backup_path': backup_path
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})