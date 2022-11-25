from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class consulting(db.Model):
    __tablename__ = 'consulting_list'