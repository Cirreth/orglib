# coding: utf-8
import json
import uuid
import datetime
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class OrderStatus(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    # Entity fields
    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    text = db.Column('text', db.String(500), nullable=False)
    create_date = db.Column('create_date', db.DateTime, nullable=False)
    user_login = db.Column(db.String(30), ForeignKey('user.login'), nullable=False)
    order_id = db.Column(db.String(36), ForeignKey('order.id'), nullable=False)

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.create_date = datetime.datetime.now()

    def __repr__(self):
        return json.dumps(self.dict_repr(), ensure_ascii=False)

    def dict_repr(self):
        return {
            'id': self.id,
            'status': self.status,
        }
