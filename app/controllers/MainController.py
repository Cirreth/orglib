from flask import render_template
from flask_login import login_required, current_user
# app
from app import app, Book


@app.route("/")
@login_required
def main():
    user_books = Book.get_by_login(current_user.login)
    last_added_books = Book.get_last(10)
    return render_template('main.html', user_books=user_books, last_added_books=last_added_books)


@app.route("/public")
@login_required
def public():
    books = Book.get_all()
    return render_template('publiclib.html', books=books)

