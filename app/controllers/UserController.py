import re
from flask import render_template, request, url_for
# app
from app import app, User
from flask_login import login_required, current_user
from webargs.flaskparser import parser
from werkzeug.utils import redirect


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    validator = User.get_input_validator()
    try:
        args = parser.parse(validator, request)
    except Exception as e:
        return render_template('user/register.html', error=str(e.data['exc'].arg_name))
    user = User()
    user.login = args['login']
    user.password = args['password']
    user.email = args['email']
    user.is_admin = False
    user.save()
    return redirect(url_for('login'))


@app.route("/users", methods=['GET'])
@login_required
def users():
    if not current_user.is_admin:
        abort(403)  # access denied
    return render_template('user/list.html', users=User.get_all())


@app.route("/user/delete/<login>", methods=['GET'])
@login_required
def user_delete(login):
    if not current_user().is_admin:
        abort(403)
    u = User.get(login)
    if not u:
        abort(404)
    u.delete()
    return redirect(url_for('admin_users'))


@app.route("/user/doadmin/<login>", methods=['GET'])
@login_required
def user_doadmin(login):
    if not current_user.is_admin:
        abort(403)
    u = User.get(login)
    if not u:
        abort(404)
    u.is_admin = True
    u.save()
    return redirect(url_for('admin_users'))
