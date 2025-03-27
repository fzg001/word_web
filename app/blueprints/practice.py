from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import WordGroup, Word, GroupStats
from app import db
import random

practice_bp = Blueprint('practice', __name__)
def get_practice_words(group, mode):
    """获取练习单词列表"""
    # 强制执行查询，获取所有单词对象
    words = list(group.words.all())  # 转换为Python列表
    
    # 调试信息
    print(f"获取到 {len(words)} 个单词，准备{mode}模式")
    
    # 确保单词列表非空
    if not words:
        return []
    
    # 如果是乱序模式，重新从数据库获取并随机排序
    if mode == 'random':
        # 获取所有单词ID
        word_ids = [word.id for word in words]
        
        # 随机打乱ID顺序
        random.shuffle(word_ids)
        
        # 重新按随机顺序获取单词
        shuffled_words = []
        for word_id in word_ids:
            word = Word.query.get(word_id)
            if word:
                shuffled_words.append(word)
                print(f"添加乱序单词: {word.english} - {word.chinese}")
        
        print(f"乱序后共 {len(shuffled_words)} 个单词")
        return shuffled_words
    
    # 顺序模式也进行ID验证，确保单词存在
    ordered_words = []
    for word in words:
        if word and Word.query.get(word.id):  # 确认单词仍存在于数据库中
            ordered_words.append(word)
            print(f"添加顺序单词: {word.english} - {word.chinese}")
    
    print(f"顺序模式共 {len(ordered_words)} 个单词")
    return ordered_words

@practice_bp.route('/study/<int:group_id>')
def study_mode(group_id):
    group = WordGroup.query.get_or_404(group_id)
    page = request.args.get('page', 1, type=int)
    
    # 创建组别特定的会话键
    session_key = f'study_{group_id}_started'
    complete_key = f'study_{group_id}_complete'
    
    # 首次进入背诵模式，设置标记但不增加计数
    if page == 1 and session_key not in session:
        session[session_key] = True
        session[complete_key] = False
        print(f"开始背诵组别: {group_id}")
    
    # 分页逻辑
    words = group.words.paginate(page=page, per_page=1)
    if not words.items:
        flash('该组别没有单词', 'warning')
        return redirect(url_for('main.index'))
    
    # 检查是否是最后一个单词
    is_last_word = (page == words.total)
    
    return render_template('study_mode.html',
                         group=group,
                         word=words.items[0],
                         current_index=page,
                         total_words=words.total,
                         is_last_word=is_last_word)


# 添加完成背诵的路由
@practice_bp.route('/complete_study/<int:group_id>')
def complete_study(group_id):
    """完成背诵，增加背诵次数"""
    group = WordGroup.query.get_or_404(group_id)
    
    # 检查会话中的标记
    session_key = f'study_{group_id}_started'
    complete_key = f'study_{group_id}_complete'
    
    # 只有开始了背诵且尚未记录完成时才增加计数
    if session.get(session_key) and not session.get(complete_key):
        group.stats.study_count += 1
        session[complete_key] = True
        db.session.commit()
        print(f"完成背诵组别: {group_id}, 当前背诵次数: {group.stats.study_count}")
        flash('背诵完成！', 'success')
    
    # 清除会话标记
    if session_key in session:
        session.pop(session_key)
    if complete_key in session:
        session.pop(complete_key)
    
    return redirect(url_for('main.index'))


@practice_bp.route('/quiz/<int:group_id>/<mode>', methods=['GET', 'POST'])
def quiz_mode(group_id, mode):
    # 创建包含组别ID的会话键
    session_key_prefix = f'quiz_{group_id}_{mode}_'
    words_key = f'{session_key_prefix}words'
    index_key = f'{session_key_prefix}index'
    correct_count_key = f'{session_key_prefix}correct_count'
    last_result_key = f'{session_key_prefix}last_result'
    correct_answer_key = f'{session_key_prefix}correct_answer'
    
    # 根据 group_id 获取 WordGroup 实例
    group = WordGroup.query.get_or_404(group_id)

    # 初始化新测试
    if words_key not in session:
        words = get_practice_words(group, mode)
        if not words:
            flash('该组别没有单词', 'warning')
            return redirect(url_for('main.index'))
        
        # 明确打印单词ID
        word_ids = []
        for word in words:
            if word and hasattr(word, 'id'):
                word_ids.append(word.id)
                print(f"添加单词ID: {word.id} ({word.english})")
        
        if not word_ids:
            flash('无法获取有效的单词ID列表', 'danger')
            return redirect(url_for('main.index'))
        
        # 保存会话数据
        session[words_key] = word_ids
        session[index_key] = 0
        session[correct_count_key] = 0
        session[last_result_key] = None
        session[correct_answer_key] = None
        
        print(f"测试初始化完成，组别: {group_id}, 模式: {mode}, 单词数: {len(word_ids)}")

    # 获取当前单词
    current_index = session[index_key]
    print(f"当前索引: {current_index}, 总单词数: {len(session[words_key])}")

    # 安全获取单词并确保它存在
    try:
        word_id = session[words_key][current_index]
        print(f"尝试获取单词ID: {word_id}")
        current_word = Word.query.get(word_id)
        
        if not current_word:
            print(f"警告: 找不到ID为 {word_id} 的单词")
            flash('单词不存在，可能已被删除', 'danger')
            return redirect(url_for('main.index'))
        
        print(f"成功获取单词: {current_word.english} - {current_word.chinese}")
    except Exception as e:
        print(f"获取单词时出错: {str(e)}")
        flash('测试数据错误，已重置', 'warning')
        keys_to_remove = [words_key, index_key, correct_count_key, last_result_key, correct_answer_key]
        for key in keys_to_remove:
            if key in session:
                session.pop(key)
        return redirect(url_for('main.index'))

    # 处理答案提交
    if request.method == 'POST' and request.form.get('answer'):
        user_answer = request.form['answer'].strip()
        
        # 再次检查当前单词是否存在（防止在提交表单时单词被删除）
        if not current_word:
            flash('单词不存在，已重置测试', 'danger')
            keys_to_remove = [words_key, index_key, correct_count_key, last_result_key, correct_answer_key]
            for key in keys_to_remove:
                if key in session:
                    session.pop(key)
            return redirect(url_for('main.index'))
            
        correct = user_answer == current_word.chinese

        # 保存当前结果信息（用于显示反馈）
        session[last_result_key] = correct
        session[correct_answer_key] = f"{current_word.english}（{current_word.chinese}）"

        # 更新统计
        session[correct_count_key] += 1 if correct else 0
        session[index_key] += 1

        # 更新数据库统计
        if mode == 'order':
            group.stats.order_quiz_count += 1
        else:
            group.stats.random_quiz_count += 1

        # 计算正确率
        total = session[index_key]
        accuracy = session[correct_count_key] / total if total > 0 else 0
        
        # 根据测试模式保存正确率
        if mode == 'order':
            group.stats.last_score = accuracy
        else:  # 乱序模式
            group.stats.random_last_score = accuracy

        db.session.commit()

        # 提交后立即检查是否已经完成所有单词
        if session[index_key] >= len(session[words_key]):
            # 清除测试相关的会话数据
            keys_to_remove = [words_key, index_key, correct_count_key, last_result_key, correct_answer_key]
            for key in keys_to_remove:
                if key in session:
                    session.pop(key)
            flash('测试完成！', 'success')
            return redirect(url_for('main.index'))

        # 获取下一个单词
        try:
            next_word_id = session[words_key][session[index_key]]
            current_word = Word.query.get(next_word_id)
            if not current_word:
                flash('无法加载下一个单词，可能已被删除', 'danger')
                return redirect(url_for('main.index'))
        except (IndexError, TypeError):
            flash('测试数据错误，已重置', 'warning')
            keys_to_remove = [words_key, index_key, correct_count_key, last_result_key, correct_answer_key]
            for key in keys_to_remove:
                if key in session:
                    session.pop(key)
            return redirect(url_for('main.index'))

    last_result = session.get(last_result_key)
    correct_answer = session.get(correct_answer_key, '')

    return render_template('quiz_mode.html',
                          group=group,
                          current_word=current_word,
                          mode=mode,
                          current_index=session[index_key] + 1,
                          total_words=len(session[words_key]),
                          last_result=last_result,
                          correct_answer=correct_answer)


@practice_bp.route('/exit_quiz/<int:group_id>/<mode>')
def exit_quiz(group_id, mode):
    """退出测试并清除会话数据"""
    # 创建包含组别ID的会话键
    session_key_prefix = f'quiz_{group_id}_{mode}_'
    words_key = f'{session_key_prefix}words'
    index_key = f'{session_key_prefix}index'
    correct_count_key = f'{session_key_prefix}correct_count'
    last_result_key = f'{session_key_prefix}last_result'
    correct_answer_key = f'{session_key_prefix}correct_answer'
    
    # 清除测试相关的会话数据
    keys_to_remove = [words_key, index_key, correct_count_key, last_result_key, correct_answer_key]
    for key in keys_to_remove:
        if key in session:
            session.pop(key)
    flash('测试已退出', 'info')
    return redirect(url_for('main.index'))