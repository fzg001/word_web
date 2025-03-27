from flask import Blueprint, render_template
from app.models import WordGroup

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # 优先按 order_index 排序，然后按创建时间排序
    groups = WordGroup.query.order_by(WordGroup.order_index, WordGroup.created_at).all()
    return render_template('index.html', groups=groups)