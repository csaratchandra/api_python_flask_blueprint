from flask import Flask
#from config import Config

#def create_app(config_class=Config):
def create_app():
    app = Flask(__name__)
#    app.config.from_object(Config)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/assignment')
    
    return app

from app import errors