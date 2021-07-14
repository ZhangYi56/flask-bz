from datetime import timedelta

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'ibm_db_sa://user:useruser123@DESKTOP-L18GBPP:50000/BZDESIGN'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    SECRET_KEY = "secretzy"
    SQLALCHEMY_BINDS = {
    'saspub': 'ibm_db_sa://048113:048113@190.2.242.173:60000/saspub'
    }

class DevelopmentConfig(Config):
    ENV = 'development'



class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
