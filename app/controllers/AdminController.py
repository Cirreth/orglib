from flask import render_template
from flask_login import login_required, current_user
# app
from app import app, User
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
    return render_template('admin/orders.html', users=[])
