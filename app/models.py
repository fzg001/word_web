from flask import request, session
from app import db
from datetime import datetime

class WordGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_index = db.Column(db.Integer, default=0)  # 添加排序字段
    is_special = db.Column(db.Boolean, default=False)
    special_type = db.Column(db.Integer, default=0)  # 1-9表示不同特殊类型
    words = db.relationship('Word', backref='group', lazy='dynamic', cascade='all, delete-orphan')
    stats = db.relationship('GroupStats', backref='group', uselist=False, cascade='all, delete-orphan')

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(100), nullable=False)
    chinese = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('word_group.id', ondelete='CASCADE'))  # 正确 
    marked = db.Column(db.Boolean, default=False)  # 标记字段，默认为0(未标记)
    deletion_mark = db.Column(db.Boolean, default=False)  # 删除标记
class GroupStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('word_group.id'), unique=True)
    study_count = db.Column(db.Integer, default=0)
    order_quiz_count = db.Column(db.Integer, default=0)
    random_quiz_count = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Float, default=0.0)  # 顺序测试正确率
    random_last_score = db.Column(db.Float, default=0.0)  # 乱序测试正确率

