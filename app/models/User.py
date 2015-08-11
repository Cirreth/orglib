# coding: utf-8
import json
import uuid
import re
from sqlalchemy import and_
from app import db


class User(db.Model):
    __tablename__ = 'user'

    # Entity fields
    id = db.Column('login', db.String(30), primary_key=True, nullable=False)
    full_name = db.Column('full_name', db.String(60), nullable=True)
    email = db.Column('email', db.String(100), nullable=False)
    is_admin = db.Column('is_admin', db.Boolean, nullable=False)

    def __repr__(self):
        return json.dumps(self.dict_repr(), ensure_ascii=False)

    def dict_repr(self):
        return {
            'login': self.login,
            'full_name': self.full_name,
            'email': self.email,
            'is_admin': self.is_admin
        }

    @classmethod
    def create_table(cls):
        cls.__table__.create(db.engine)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.full_name).all()

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
