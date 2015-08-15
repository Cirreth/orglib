# coding: utf-8
import json
import re
import uuid
import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from webargs import Arg


class Order(db.Model):

    # Entity fields
    id = db.Column('id', db.String(36), primary_key=True, nullable=False)
    author = db.Column('author', db.Integer, nullable=False)
    name = db.Column('name', db.String(300), nullable=False)
    year = db.Column('year', db.Integer, nullable=True)
    create_date = db.Column('create_date', db.DateTime, nullable=False)
    user_login = db.Column(db.String(30), ForeignKey('user.login'), nullable=False)
    user = relationship('User')
    status_id = db.Column(db.Integer, ForeignKey('order_status.id'), nullable=False)
    status = relationship('OrderStatus')
    book_id = db.Column(db.String(36), ForeignKey('book.id'), nullable=True)
    book = relationship('Book')
    # comments = relationship('Comment')

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.status_id = 0  # initial
        self.create_date = datetime.datetime.now()

    def __repr__(self):
        return json.dumps(self.dict_repr(), ensure_ascii=False)

    def dict_repr(self):
        return {
            'id': self.id,
            'author': self.author,
            'name': self.name,
            'year': self.year,
            'create_date': self.create_date.strftime('%d.%m.%Y %H:%M:%S')
        }

    @classmethod
    def get_input_validator(cls):
        return {
            'author': Arg(str, required=True, validate=lambda p: len(p) > 0),
            'name': Arg(str, required=True, validate=lambda p: len(p) > 0),
            'year': Arg(str, required=False, validate=lambda p: re.match(r'^\d{4}$|^$', p) is not None)
        }

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
