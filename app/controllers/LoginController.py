from app.models import User
from flask import request, render_template, url_for, session
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user
from werkzeug.utils import redirect
from app import app

login_manager = LoginManager()
login_manager.init_app(app)


def redirect_login():
    return redirect(url_for('login'))

login_manager.unauthorized_handler(redirect_login)


@login_manager.user_loader
def load_user(lgn):
    return User.get(lgn)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        lgn = request.form['login']
        pwd = request.form['password']
        user = load_user(lgn)
        if user and pwd == user.password:
            login_user(user)
            return redirect(url_for('main'))
        return render_template('login.html', error='Неверный пароль или пользователь не существует')
    else:
        return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))