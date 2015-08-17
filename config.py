import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
# TESTING = True
JSON_AS_ASCII = False
WERKZEUG_LOGGING = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'orglib.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
CSRF_ENABLED = True
SECRET_KEY = '59C7D9A3-E23C-4D97-A37B-B11CE4CD6848'
UPLOAD_FOLDER = os.path.join(basedir, 'static/books')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])