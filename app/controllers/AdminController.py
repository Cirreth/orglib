from flask import render_template
from flask_login import login_required, current_user
# app
from app import app, User, Order
from webargs.flaskparser import abort


@app.route("/admin/users")
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)  # access denied
    users = User.get_all()
    return render_template('admin/users.html', users=users)


@app.route("/admin/orders")
@login_required
def admin_orders():
    if not current_user.is_admin:
        abort(403)  # access denied
    ods = Order.get_all()
    return render_template('admin/orders.html', orders=ods)


@app.route("/admin/order/<order_id>", methods=['GET'])
@login_required
def admin_order(order_id):
    if not current_user.is_admin:
        abort(403)  # access denied
    o = Order.get(order_id)
    return render_template('admin/order.html', o=o)
