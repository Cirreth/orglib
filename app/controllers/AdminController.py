from flask import render_template
from flask_login import login_required
# app
from app import app, User


@app.route("/admin/users")
@login_required
def admin_users():
    users = User.get_all()
    return render_template('admin/users.html', users=users)
