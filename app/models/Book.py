# coding: utf-8
import json
import re
import uuid
from app import db
from webargs import Arg


class Book(db.Model):

    # Entity fields
    id = db.Column('id', db.String(36), primary_key=True, nullable=False)
    author = db.Column('author', db.Integer, nullable=False)
    name = db.Column('name', db.String(300), nullable=False)
    year = db.Column('year', db.Integer, nullable=False)
    file = db.Column('file', db.Boolean, nullable=False)

    def __init__(self):
        self.id = str(uuid.uuid4())

    def __repr__(self):
        return json.dumps(self.dict_repr(), ensure_ascii=False)

    def dict_repr(self):
        return {
            'id': self.id,
            'author': self.author,
            'name': self.name,
            'year': self.year,
            'file': self.file
        }

    @classmethod
    def get_input_validator(cls):
        return {
            'author': Arg(str, required=True, validate=lambda p: len(p) > 0),
            'name': Arg(str, required=True, validate=lambda p: len(p) > 0),
            'year': Arg(str, required=True, validate=lambda p: re.match(r'^\d{4}$', p) is not None),
            'file': Arg(str, required=True, validate=lambda p: re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z0-9]{1,4}$', p) is not None)
        }

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    # @classmethod
    # def get_filtered(cls, filter_str, page=0, page_size=10):
    #     return cls.query \
    #         .filter(cls.full_name.ilike('%' + filter_str + '%')) \
    #         .order_by(cls.full_name) \
    #         .offset(page * page_size) \
    #         .limit(page_size) \
    #         .all()
    #
    # @classmethod
    # def get_filtered_count(cls, filter_str):
    #     return cls.query.filter(cls.full_name.ilike('%' + filter_str + '%')).count()

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

