import re
from flask import render_template, request, url_for
# app
from app import app, Book
from flask_login import login_required, current_user
from webargs.flaskparser import parser, abort
from werkzeug.utils import redirect


@app.route("/books/create", methods=['GET', 'POST'])
@login_required
def book_create():
    if request.method == 'GET':
        return render_template('book/create.html')
    validator = Book.get_input_validator()
    try:
        args = parser.parse(validator, request)
    except Exception as e:
        return render_template('book/create.html', error=str(e.data['exc'].arg_name))
    book = Book()
    book.author = args['author']
    book.name = args['name']
    book.year = args['year']
    book.file = args['file']
    book.added_by_login = current_user.login
    book.save()
    return redirect(url_for('main'))


@app.route("/book/<book_id>/delete", methods=['GET'])
@login_required
def book_delete(book_id):
    if not current_user.is_admin:
        abort(403)
    b = Book.get(book_id)
    if not b:
        abort(404)
    b.delete()
    return redirect(url_for('admin_public'))


@app.route("/book/<book_id>/share", methods=['GET'])
@login_required
def book_share(book_id):
    b = Book.get(book_id)
    if not b:
        abort(404)
    if not b.added_by_login != current_user.login:
        abort(403)
    b.is_public = not b.is_public
    b.save()
    return redirect(url_for('public'))
