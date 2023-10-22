from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from fast_bitrix24 import Bitrix
import base64

BitrixQ = 'aHR0cHM6Ly92YzFjLmJpdHJpeDI0LnJ1L3Jlc3QvNDc5L21qbWRpNXczd3ZsOWpvNWcvCg=='
webhook = base64.b64decode(BitrixQ).decode('utf-8')
B = Bitrix(webhook)
  

# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

'''
sentry_sdk.init(
    dsn="https://5a6b1a7f3d23458fa751de233db25cd0@o4505186652717056.ingest.sentry.io/4505186654289920",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

'''
app = Flask(__name__)
app.secret_key = 'some very secret phrase for web_app_4dk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/application/mods/DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from mods import models
from mods import routes



