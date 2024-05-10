from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app, version='2.0', title='FarmBot API',
          description='Different endpoints for the FarmBot, SmartGreenhouse and Weather Station')
