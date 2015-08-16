# coding: utf-8
import json
import uuid
import datetime
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Comment(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    # Entity fields
    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    text = db.Column('text', db.String(500), nullable=False)
    unread = db.Column('unread', db.Boolean, nullable=False)
    create_date = db.Column('create_date', db.DateTime, nullable=False)
    user_login = db.Column(db.String(30), ForeignKey('user.login'), nullable=False)
    user = db.relationship('User')
    order_id = db.Column(db.String(36), ForeignKey('order.id'), nullable=False)

    def __init__(self):
        self.unread = True
        self.create_date = datetime.datetime.now()

    def __repr__(self):
        return json.dumps(self.dict_repr(), ensure_ascii=False)

    def dict_repr(self):
        return {
            'id': self.id,
            'status': self.status,
        }

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.create_date).all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e