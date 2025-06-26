from db import db
from db import db
from datetime import datetime


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)   
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'created_at': self.created_at       
        }

class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    type = db.Column(db.String(7), nullable=False)
    amount = db.Column(db.Float, default=False, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def to_dict(self):
        return {
        'id': self.id,
        'user_id': self.user_id,
        'type': self.type,
        'amount': self.amount,
        'category': self.category,
        'date': self.date,       
        }

