from flask import request, render_template, url_for, session
from flask_login import LoginManager, login_user, UserMixin
from werkzeug.utils import redirect
from app import app

login_manager = LoginManager()
login_manager.init_app(app)


def redirect_login():
    return redirect(url_for('login'))

login_manager.unauthorized_handler(redirect_login)


class User(UserMixin):

    @classmethod
    def get(cls, code):
        if code.lower() == '123':
            u = User()
            u.id = code
            return u


@login_manager.user_loader
def load_user(code):
    return User.get(code)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        code = request.form['code']
        try:
            login_user(load_user(code))
        except Exception as e:
            return render_template('login.html', error='Неверный пароль')
        return redirect(url_for('main'))
    else:
        return render_template('login.html')
