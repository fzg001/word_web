from flask import Blueprint, render_template
from app.models import WordGroup

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    groups = WordGroup.query.all()
    return render_template('index.html', groups=groups)