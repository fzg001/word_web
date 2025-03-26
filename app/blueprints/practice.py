from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import WordGroup, Word, GroupStats
from app import db
import random

practice_bp = Blueprint('practice', __name__)

def get_practice_words(group, mode):
    """获取练习单词列表"""
    words = list(group.words)
    if mode == 'random':
        random.shuffle(words)
    return words

@practice_bp.route('/study/<int:group_id>')
def study_mode(group_id):
    group = WordGroup.query.get_or_404(group_id)
    page = request.args.get('page', 1, type=int)
    
    # 更新学习次数统计
    group.stats.study_count += 1
    db.session.commit()
    
    # 分页逻辑
    words = group.words.paginate(page=page, per_page=1)
    if not words.items:
        flash('该组别没有单词', 'warning')
        return redirect(url_for('main.index'))
    
    return render_template('study_mode.html',
                         group=group,
                         word=words.items[0],
                         current_index=page,
                         total_words=words.total)


@practice_bp.route('/quiz/<int:group_id>/<mode>', methods=['GET', 'POST'])
def quiz_mode(group_id, mode):
    # 根据 group_id 获取 WordGroup 实例
    group = WordGroup.query.get_or_404(group_id)

    # 处理 reset 参数
    if request.method == 'GET' and request.args.get('reset') == '1':
        # 只清除测试相关的会话数据
        keys_to_remove = [f'quiz_words_{mode}', f'current_index_{mode}', f'correct_count_{mode}', f'last_result_{mode}', f'correct_answer_{mode}']
        for key in keys_to_remove:
            if key in session:
                session.pop(key)
        return redirect(url_for('main.index'))

    # 初始化新测试
    if f'quiz_words_{mode}' not in session:
        words = get_practice_words(group, mode)
        session[f'quiz_words_{mode}'] = [w.id for w in words]
        session[f'current_index_{mode}'] = 0
        session[f'correct_count_{mode}'] = 0
        session[f'last_result_{mode}'] = None
        session[f'correct_answer_{mode}'] = None

    # 获取当前单词
    current_index = session[f'current_index_{mode}']

    # 如果已经完成所有单词，清除会话并返回首页
    if current_index >= len(session[f'quiz_words_{mode}'] ):
        # 清除测试相关的会话数据
        keys_to_remove = [f'quiz_words_{mode}', f'current_index_{mode}', f'correct_count_{mode}', f'last_result_{mode}', f'correct_answer_{mode}']
        for key in keys_to_remove:
            if key in session:
                session.pop(key)
        flash('测试完成！', 'success')
        return redirect(url_for('main.index'))

    word_id = session[f'quiz_words_{mode}'] [current_index]
    current_word = Word.query.get(word_id)

    # 处理答案提交
    if request.method == 'POST' and request.form.get('answer'):
        user_answer = request.form['answer'].strip()
        correct = user_answer == current_word.chinese

        # 保存当前结果信息（用于显示反馈）
        session[f'last_result_{mode}'] = correct
        # 修改这里，同时保存英文和中文
        session[f'correct_answer_{mode}'] = f"{current_word.english}（{current_word.chinese}）"

        # 更新统计
        session[f'correct_count_{mode}'] += 1 if correct else 0
        session[f'current_index_{mode}'] += 1

        # 更新数据库统计
        if mode == 'order':
            group.stats.order_quiz_count += 1
        else:
            group.stats.random_quiz_count += 1

        # 计算正确率
        # 计算正确率
        total = session[f'current_index_{mode}']
        accuracy = session[f'correct_count_{mode}'] / total if total > 0 else 0
        group.stats.last_score = accuracy
        # 根据测试模式保存正确率
        if mode == 'order':
            group.stats.last_score = accuracy
        else:  # 乱序模式
            group.stats.random_last_score = accuracy

        db.session.commit()

        # 关键修改：提交后立即检查是否已经完成所有单词
        if session[f'current_index_{mode}'] >= len(session[f'quiz_words_{mode}'] ):
            # 清除测试相关的会话数据
            keys_to_remove = [f'quiz_words_{mode}', f'current_index_{mode}', f'correct_count_{mode}', f'last_result_{mode}', f'correct_answer_{mode}']
            for key in keys_to_remove:
                if key in session:
                    session.pop(key)
            flash('测试完成！', 'success')
            return redirect(url_for('main.index'))

        # 获取下一个单词
        next_word_id = session[f'quiz_words_{mode}'] [session[f'current_index_{mode}']]
        current_word = Word.query.get(next_word_id)

    last_result = session.get(f'last_result_{mode}')
    correct_answer = session.get(f'correct_answer_{mode}', '')

    return render_template('quiz_mode.html',
                          group=group,
                          current_word=current_word,
                          mode=mode,
                          current_index=session[f'current_index_{mode}']  + 1,
                          total_words=len(session[f'quiz_words_{mode}']),
                          last_result=last_result,
                          correct_answer=correct_answer)

@practice_bp.route('/exit_quiz/<mode>')
def exit_quiz(mode):
    """退出测试并清除会话数据"""
    # 清除测试相关的会话数据
    keys_to_remove = [f'quiz_words_{mode}', f'current_index_{mode}', f'correct_count_{mode}', f'last_result_{mode}', f'correct_answer_{mode}']
    for key in keys_to_remove:
        if key in session:
            session.pop(key)
    flash('测试已退出', 'info')
    return redirect(url_for('main.index'))