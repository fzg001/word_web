from flask import Blueprint, jsonify, current_app, request
from sqlalchemy import inspect
from app.models import WordGroup, Word, db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/groups')
def get_groups():
    """返回所有组的基本信息，用于全局搜索"""
    try:
        # 正确检查数据库表
        inspector = inspect(db.engine)
        if not inspector.has_table('word_group'):
            return jsonify({
                'success': False, 
                'message': '数据库中不存在word_group表',
                'groups': []
            })
        
        # 查询所有组
        groups = WordGroup.query.all()
        current_app.logger.info(f"查询到 {len(groups)} 个单词组")
        
        groups_data = [
            {
                'id': group.id,
                'name': group.name,
                'word_count': group.words.count() if hasattr(group, 'words') else 0,
                'level': group.level if hasattr(group, 'level') else 'basic'
            }
            for group in groups
        ]
        return jsonify({'success': True, 'groups': groups_data})
    
    except Exception as e:
        current_app.logger.error(f"获取组数据时出错: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f"获取单词组数据失败: {str(e)}",
            'groups': []
        })

# 保留测试接口
@api_bp.route('/test')
def api_test():
    """简单的测试接口，确认API能够工作"""
    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        # 检查数据库内容
        group_count = WordGroup.query.count()
        word_count = Word.query.count()
        
        return jsonify({
            'success': True,
            'message': 'API正常工作',
            'database_tables': tables,
            'database_uri': str(db.engine.url).replace('://', '://***:***@'),
            'group_count': group_count,
            'word_count': word_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'API测试失败: {str(e)}'
        })

@api_bp.route('/search_groups')
def search_groups():
    """根据查询字符串搜索单词组"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'success': True, 'groups': []})
    
    try:
        # 从数据库中搜索匹配的组
        groups = WordGroup.query.filter(WordGroup.name.ilike(f'%{query}%')).limit(10).all()
        
        groups_data = [
            {
                'id': group.id,
                'name': group.name,
                'word_count': group.words.count(),
                'level': group.level if hasattr(group, 'level') else 'basic'
            }
            for group in groups
        ]
        
        return jsonify({'success': True, 'groups': groups_data})
    except Exception as e:
        current_app.logger.error(f"搜索单词组时出错: {str(e)}")
        return jsonify({'success': False, 'message': str(e), 'groups': []})