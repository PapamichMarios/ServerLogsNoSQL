from flask import Flask
from .extensions import mongo

from .methods import methods
from .insert import insert

def create_app(config_object='ServerLogsNoSQL.settings'):
    
    app = Flask(__name__)
    # app.config.from_object(config_object)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/log_db"
    mongo.init_app(app)

    # register controllers
    app.register_blueprint(methods)
    app.register_blueprint(insert)
    
    return app
if __name__=='__main__':
    app = create_app()
    app.debug = True
    app.run(host='0.0.0.0',port=5000)