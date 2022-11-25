from LMS import app
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

# class User(db.Model):
#     __table__name =

# @app.route('/')
# def login():
#     return render_template('login.html')

# @app.route('/perform')
# def perform():
#     return render_template('perform.html')
#
# @app.route('/user')
# def get_user_manage():
#     return render_template('user.html')
#
# app.run(host='localhost')
