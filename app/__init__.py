from flask import Flask, send_from_directory
from flask_pymongo import PyMongo
from config import Config
import os

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

   
    mongo.init_app(app)

    with app.app_context():
        mongo.db = mongo.cx["image_processor"]  # Set your actual database name

    from app.celery import init_celery, celery
    init_celery(app)

    from app.routes import bp  
    app.register_blueprint(bp)

    return app
