from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import WordGroup, Word, GroupStats
from app.utils.validation import validate_word_input

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/create', methods=['GET', 'POST'])
def create_group(word_processing_errors=None):
    """创建新的单词组"""
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        words_text = request.form.get('words')
        
        # 验证输入
        if not group_name or not words_text:
            flash('组名和单词内容不能为空', 'danger')
            return redirect(url_for('groups.create_group'))
        
        # 创建新组别
        group = WordGroup(name=group_name)
        db.session.add(group)
        
        try:
            db.session.flush()  # 获取组别ID但不提交
            
            # 解析并添加单词
            word_count = 0
            error_lines = []
            
            for line_number, line in enumerate(words_text.splitlines(), 1):
                line = line.strip()
                if not line:  # 跳过空行
                    continue
                    
                eng, chn = validate_word_input(line)
                if eng and chn:
                    word = Word(english=eng, chinese=chn, group_id=group.id)
                    db.session.add(word)
                    word_count += 1
                else:
                    error_lines.append(f"第 {line_number} 行: '{line}'")
            
            # 检查是否至少有一个有效单词
            if word_count == 0:
                db.session.rollback()
                flash('未找到有效单词，请检查输入格式', 'danger')
                return render_template('create_group.html', 
                                      error_lines=error_lines,
                                      group_name=group_name,
                                      words_text=words_text)
            
            # 创建统计记录
            stats = GroupStats(group_id=group.id)
            db.session.add(stats)
            
            db.session.commit()
            
            if error_lines:
                flash(f'创建成功，但有 {len(error_lines)} 行无法解析', 'warning')
                return render_template('create_group.html', 
                                      error_lines=error_lines,
                                      success_message=f'已成功添加 {word_count} 个单词到组别 "{group_name}"')
            else:
                flash(f'创建成功！已添加 {word_count} 个单词', 'success')
                return redirect(url_for('main.index'))
                
        except Exception as e:
            db.session.rollback()
            flash(f'创建失败: {str(e)}', 'danger')
            return redirect(url_for('groups.create_group'))
    
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