from todoapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    

    def __repr__(self):#how our object is printed whenever its printed out
        return f"User('{self.username}', '{self.email}')"

# create model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Text, nullable=False)
    duedate= db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    complete = db.Column(db.Boolean)