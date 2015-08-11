import re
from flask import render_template, request, url_for
# app
from app import app, User
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
    user.full_name = args['fullName']
    user.email = args['email']
    user.is_admin = False
    user.save()
    return redirect(url_for('login'))


@app.route("/users", methods=['GET'])
def users():
    return render_template('user/list.html', users=User.get_all())