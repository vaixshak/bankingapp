from extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    account_number = db.Column(db.BigInteger, unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)  
