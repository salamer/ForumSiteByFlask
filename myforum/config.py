import os

class Config:
    SECRET_KEY=os.environ.get('SECRECT_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
#    FLASKY_MAIL_SUBJECT_PREFI='[Flasky]'
#    FLASKY_MAIL_SENDER='Flasky admin <flasky@example.com>'
    FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')
    FLASKY_FOLLOWERS_PER_PAGE=50
    FLASKY_COMMENTS_PER_PAGE=10
    @staticmethod
    def init_app(app):
        pass
        
class DevelopmentConfig(Config):
    DEBUG=True
    
#    MAIL_SERVER='smtp.googlemail.com'
#    MAIN_PORT=587
#    MAIL_USE_TLS=True
#    MAIL_USERNAME=os.environ.egt('MAIL_USERNAME')
#    MAIN_PASSWORD=os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI='mysql://root:960219@localhost/devmyflasky'
    
class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='mysql://root:960219@localhost/testmyflasky'
    
class ProductionConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='mysql://root:960219@localhost/myflasky'
    
config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    
    'default':DevelopmentConfig
}
