from flask import Blueprint, render_template, redirect, url_for, current_app
from app.models import Word, WordGroup, GroupStats, db

special_bp = Blueprint('special', __name__, url_prefix='/special')

@special_bp.route('/')
def index():
    """显示特殊组别页面"""
    # 获取所有标记的单词数量
    marked_words_count = Word.query.filter_by(marked=True).count()
    
    # 查询现有的特殊组（如果存在）
    obsidian_group = WordGroup.query.filter_by(name="黑曜石收藏").first()
    
    return render_template(
        'special_groups.html', 
        marked_words_count=marked_words_count,
        obsidian_group=obsidian_group
    )

@special_bp.route('/obsidian/practice/<mode>')
def obsidian_practice(mode):
    """使用标记的单词进行练习"""
    # 获取或创建黑曜石组
    obsidian_group = WordGroup.query.filter_by(name="黑曜石收藏").first()
    
    if not obsidian_group:
        # 创建新组并标记为特殊组
        obsidian_group = WordGroup(
            name="黑曜石收藏", 
            is_special=True,
            special_type=1
        )
        db.session.add(obsidian_group)
        db.session.flush()  # 获取ID但不提交
        
        # 创建统计记录
        stats = GroupStats(group_id=obsidian_group.id)
        db.session.add(stats)
        
        # 添加所有标记的单词
        marked_words = Word.query.filter_by(marked=True).all()
        for word in marked_words:
            # 创建新单词对象关联到新组
            new_word = Word(
                english=word.english,
                chinese=word.chinese,
                group_id=obsidian_group.id,
                marked=True
            )
            db.session.add(new_word)
        
        db.session.commit()
    else:
        # 更新所有标记的单词
        update_obsidian_words(obsidian_group)
        
        # 确保有统计记录
        if not obsidian_group.stats:
            stats = GroupStats(group_id=obsidian_group.id)
            db.session.add(stats)
            db.session.commit()
    
    # 根据模式重定向到相应的练习页面
    if mode == 'study':
        return redirect(url_for('practice.study_mode', group_id=obsidian_group.id))
    elif mode == 'order':
        return redirect(url_for('practice.quiz_mode', group_id=obsidian_group.id, mode='order'))
    elif mode == 'random':
        return redirect(url_for('practice.quiz_mode', group_id=obsidian_group.id, mode='random'))
    
    return redirect(url_for('special.index'))

def update_obsidian_words(obsidian_group):
    """更新黑曜石卡片的单词列表，确保包含所有标记的单词，并移除不再标记的单词"""
    # 获取所有标记单词
    all_marked_words = Word.query.filter_by(marked=True).all()
    marked_word_dict = {(w.english, w.chinese): w for w in all_marked_words}
    
    # 获取当前黑曜石组中的单词
    current_words = obsidian_group.words.all()
    current_word_dict = {(w.english, w.chinese): w for w in current_words}
    
    # 添加新标记的单词
    for key, word in marked_word_dict.items():
        if key not in current_word_dict:
            print(f"添加单词到黑曜石收藏: {word.english} - {word.chinese}")
            new_word = Word(
                english=word.english,
                chinese=word.chinese,
                group_id=obsidian_group.id,
                marked=True
            )
            db.session.add(new_word)
    
    # 移除已取消标记的单词
    for key, word in current_word_dict.items():
        if key not in marked_word_dict:
            print(f"从黑曜石收藏移除单词: {word.english} - {word.chinese}")
            db.session.delete(word)
    
    # 提交更改
    db.session.commit()
    
    # 更新黑曜石组信息
    obsidian_group.is_special = True
    obsidian_group.special_type = 1
    db.session.commit()