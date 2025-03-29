from app import create_app, db
from app.models import WordGroup

app = create_app()

def fix_obsidian_group():
    """修复黑曜石组类型"""
    with app.app_context():
        obsidian = WordGroup.query.filter_by(name="黑曜石收藏").first()
        if obsidian:
            obsidian.is_special = True
            obsidian.special_type = 1
            db.session.commit()
            print(f"已修复黑曜石组: is_special={obsidian.is_special}, special_type={obsidian.special_type}")
        else:
            print("未找到黑曜石收藏组")

if __name__ == "__main__":
    fix_obsidian_group()