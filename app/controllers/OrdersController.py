import re
from flask import render_template, request, url_for
# app
from app import app, Book
from webargs.flaskparser import parser
from werkzeug.utils import redirect


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        return render_template('order/orders.html')


@app.route("/orders/create", methods=['GET', 'POST'])
def order_create():
    if request.method == 'GET':
        return render_template('order/create.html')