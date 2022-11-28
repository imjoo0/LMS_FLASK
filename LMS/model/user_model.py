from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import app

db=SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(id.Integer,primary_key=True)

class consulting(db.Model):
    __tablename__ = 'consulting_list'