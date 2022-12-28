class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:secret22liz@localhost/forum'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///elem.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'itsreptextoflovemcpirog'