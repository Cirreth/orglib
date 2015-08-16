import re
from flask import render_template, request, url_for
# app
from app import app, Order
from flask_login import current_user, login_required
from webargs.flaskparser import parser, abort
from werkzeug.utils import redirect


@app.route("/orders", methods=['GET', 'POST'])
@login_required
def orders():
    if request.method == 'GET':
        ods = current_user.orders
        return render_template('order/orders.html', orders=ods)


@app.route("/orders/create", methods=['GET', 'POST'])
@login_required
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
    o.user_login = current_user.login
    o.save()
    return redirect(url_for('orders'))


@app.route("/order/<order_id>", methods=['GET'])
@login_required
def order(order_id):
    o = Order.get(order_id)
    return render_template('order/order.html', o=o)
