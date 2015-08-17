from flask import render_template, url_for
from flask_login import login_required, current_user
# app
from app import app, User, Order, OrderStatus, Book
from webargs.flaskparser import abort
from werkzeug.utils import redirect


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


@app.route("/admin/order/<order_id>/set-status/<new_status_code>", methods=['GET'])
@login_required
def admin_order_set_status(order_id, new_status_code):
    if not current_user.is_admin:
        abort(403)  # access denied
    o = Order.get(order_id)
    if not OrderStatus.get(new_status_code):
        return abort(400)  # bad request
    o.status_id = new_status_code
    o.save()
    return redirect(url_for('admin_order', order_id=order_id))


@app.route("/admin/public")
@login_required
def admin_public():
    books = Book.get_public()
    return render_template('/admin/publiclib.html', books=books)

