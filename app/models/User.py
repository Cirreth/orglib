# coding: utf-8
import json
import re
from app import db
from flask_login import UserMixin
from webargs import Arg


users_books = db.Table('users_book',
    db.Column('user_login', db.Integer, db.ForeignKey('user.login')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)


class User(db.Model, UserMixin):
    # Entity fields
    login = db.Column('login', db.String(30), primary_key=True, nullable=False)
    password = db.Column('password', db.String(30), nullable=False)
    email = db.Column('email', db.String(100), nullable=False)
    is_admin = db.Column('is_admin', db.Boolean, nullable=False)
    books = db.relationship('Book',
                            secondary=users_books,
                            primaryjoin=(users_books.c.user_login == login),
                            backref=db.backref('users_books', lazy='dynamic'),
                            lazy='dynamic')
    orders = db.relationship('Order')

    def __repr__(self):
        return json.dumps(self.dict_repr(), ensure_ascii=False)

    def dict_repr(self):
        return {
            'login': self.login,
            'password': self.password,
            'email': self.email,
            'is_admin': self.is_admin
        }

    def get_id(self):
        return self.login

    @classmethod
    def get_input_validator(cls):
        return {
            'login': Arg(str, required=True, validate=lambda p: re.match(r'^[a-zA-Z]+[a-zA-Z0-9]*$', p) is not None),
            'password': Arg(str, required=True, validate=lambda p: re.match(r'^.{3,}$', p) is not None),
            'email': Arg(str, required=True, validate=lambda p: re.match(r'.*@.*', p) is not None)
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

    def has_book(self, book):
        return self.books.filter(users_books.c.book_id == book.id).count() > 0

    def get_books(self):
        return self.books.filter(users_books.c.user_login == self.login).all()

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
