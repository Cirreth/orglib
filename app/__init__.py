from flask import Flask, url_for
from flask_login import login_required
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__, template_folder='..//templates', static_folder='../static')

app.config.from_object('config')

# SQLAlchemy
db = SQLAlchemy(app)

# migrations
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# import app objects
from app.models import *
from app.controllers import *


# all other routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def catch_all(path):
    return redirect(url_for('main'))
