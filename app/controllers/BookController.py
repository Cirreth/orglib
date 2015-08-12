import re
from flask import render_template, request, url_for
# app
from app import app, Book
from webargs.flaskparser import parser
from werkzeug.utils import redirect


@app.route("/books/create", methods=['GET', 'POST'])
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
    book.save()
    return redirect(url_for('main'))