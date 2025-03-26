from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import WordGroup, Word, GroupStats
from app.utils.validation import validate_word_input

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/create', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        words_text = request.form.get('words')
        
        # 验证输入
        if not group_name or not words_text:
            flash('组名和单词内容不能为空', 'danger')
            return redirect(url_for('groups.create_group'))
        
        # 处理单词输入
        words = []
        for line in words_text.split('\n'):
            line = line.strip()
            if line:
                eng, chn = validate_word_input(line)
                if eng and chn:
                    words.append(Word(english=eng, chinese=chn))
        
        # 创建组别
        new_group = WordGroup(name=group_name)
        new_group.words = words
        new_group.stats = GroupStats()
        
        db.session.add(new_group)
        try:
            db.session.commit()
            flash('组别创建成功', 'success')
            return redirect(url_for('main.index'))
        except:
            db.session.rollback()
            flash('组别名称已存在', 'danger')
    
    return render_template('create_group.html')

@groups_bp.route('/<int:group_id>')
def group_detail(group_id):
    group = WordGroup.query.get_or_404(group_id)
    return render_template('group_detail.html', group=group)


@groups_bp.route('/manage')
def manage_groups():
    """显示所有组别管理页面"""
    groups = WordGroup.query.all()
    return render_template('manage_groups.html', groups=groups)

@groups_bp.route('/<int:group_id>/edit', methods=['GET', 'POST'])
def edit_group(group_id):
    """编辑单词组"""
    group = WordGroup.query.get_or_404(group_id)
    
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        words_text = request.form.get('words')
        
        # 验证输入
        if not group_name or not words_text:
            flash('组名和单词内容不能为空', 'danger')
            return redirect(url_for('groups.edit_group', group_id=group_id))
        
        # 更新组名
        group.name = group_name
        
        # 清除现有单词
        Word.query.filter_by(group_id=group_id).delete()
        
        # 添加新单词
        for line in words_text.split('\n'):
            line = line.strip()
            if line:
                eng, chn = validate_word_input(line)
                if eng and chn:
                    word = Word(english=eng, chinese=chn, group_id=group_id)
                    db.session.add(word)
        
        try:
            db.session.commit()
            flash('组别更新成功', 'success')
            return redirect(url_for('groups.manage_groups'))
        except:
            db.session.rollback()
            flash('更新失败，组名可能已存在', 'danger')
    
    # 准备单词文本用于编辑
    words_text = '\n'.join([f"{word.english} - {word.chinese}" for word in group.words])
    
    return render_template('edit_group.html', group=group, words_text=words_text)

@groups_bp.route('/<int:group_id>/delete', methods=['POST'])
def delete_group(group_id):
    """删除单词组"""
    group = WordGroup.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    flash('组别已删除', 'success')
    return redirect(url_for('groups.manage_groups'))