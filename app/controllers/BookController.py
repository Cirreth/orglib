import os
from flask import render_template, request, url_for, jsonify
# app
from app import app, Book
from flask_login import login_required, current_user
from webargs.flaskparser import parser, abort
from werkzeug.utils import redirect


@app.route('/books/json/public')
@login_required
def book_public_json():
    books = Book.get_public()
    return jsonify({"books": [{"id": b.id, "text": b.author + " - " + b.name} for b in books]})


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
    # file
    file = request.files['file']
    extension = file.filename.split('.')[-1] or ""
    book.file = book.id + '.' + extension
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], book.file))
    #
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
    if b.added_by_login != current_user.login:
        abort(403)
    b.is_public = not b.is_public
    b.save()
    return redirect(url_for('main'))


@app.route("/book/<book_id>/get", methods=['GET'])
@login_required
def book_get(book_id):
    b = Book.get(book_id)
    if not b:
        abort(404)
    if not b.is_public:
        abort(403)
    if not current_user.has_book(b):
        current_user.books.append(b)
        current_user.save()
    return redirect(url_for('public'))


@app.route("/book/<book_id>/remove", methods=['GET'])
@login_required
def book_remove(book_id):
    b = Book.get(book_id)
    if not b:
        abort(404)
    if not b.is_public:
        abort(403)
    if current_user.has_book(b):
        current_user.books.remove(b)
        current_user.save()
    return redirect(url_for('main'))
