class Config:
    DEBUG = True
    # TESTING = True
    JSON_AS_ASCII = False
    WERKZEUG_LOGGING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../orglib.db'
    CSRF_ENABLED = True
    SECRET_KEY = '59C7D9A3-E23C-4D97-A37B-B11CE4CD6848'


class ProductionConfig(Config):
    pass
