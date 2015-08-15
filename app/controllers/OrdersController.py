import re
from flask import render_template, request, url_for
# app
from app import app, Order
from webargs.flaskparser import parser
from werkzeug.utils import redirect


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        return render_template('order/orders.html')


@app.route("/orders/create", methods=['GET', 'POST'])
def order_create():
    if request.method == 'GET':
        return render_template('order/create.html', model={})
    # POST
    validator = Order.get_input_validator()
    try:
        args = parser.parse(validator, request)
    except Exception as e:
        return render_template('order/create.html', error=str(e.data['exc'].arg_name), model=request.form)
    o = Order()
    o.author = args['author']
    o.name = args['name']
    o.year = args['year']
    o.save()
    return redirect(url_for('orders'))
