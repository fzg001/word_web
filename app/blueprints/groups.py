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