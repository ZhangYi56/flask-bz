
from re import template
from settings import DevelopmentConfig,ProductionConfig
from exts import db
from flask import Flask 
from apps.indexbp.view import index_bp
from apps.lock.view import lock_bp
from apps.material_tracking.mt import mt_bp



def create_app():
    app =Flask(__name__, template_folder='../templates',static_folder='../static')
    app.config.from_object(ProductionConfig)

    db.init_app(app=app)
    app.register_blueprint(index_bp)
    app.register_blueprint(lock_bp, url_prefix= '/lock50')
    app.register_blueprint(mt_bp, url_prefix= '/material_tracking')

    return app
