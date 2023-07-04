from flask import Flask
from flask_restful import Api, Resource
from pymongo import MongoClient
import smtplib
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://localhost:27017")
db = client['UserDB']
collection = db['UserCollection']
app.config["JWT_SECRET_KEY"] = "zanchanotachi"
jwt_manager = JWTManager(app)
