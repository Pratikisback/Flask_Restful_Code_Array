from flask import Flask
from flask_restful import Api, Resource
from pymongo import MongoClient
import smtplib


app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://localhost:27017")
db = client['UserDB']
collection = db['UserCollection']
