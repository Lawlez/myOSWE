from flask import Flask
from application.blueprints.routes import web, api

app = Flask(__name__)
app.config.from_object('application.config.Config')

app.register_blueprint(web, url_prefix='/')
app.register_blueprint(api, url_prefix='/api')

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not Found'}, 404