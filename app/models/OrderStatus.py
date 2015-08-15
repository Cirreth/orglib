# coding: utf-8
import json
from app import db


class OrderStatus(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    # Entity fields
    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    status = db.Column('status', db.String(50), nullable=False)

    def __repr__(self):
        return json.dumps(self.dict_repr(), ensure_ascii=False)

    def dict_repr(self):
        return {
            'id': self.id,
            'status': self.status,
        }
