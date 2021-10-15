from sqlalchemy.orm import backref
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
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    task = db.relationship('Todo', backref='user', lazy=True)
    #our task attribute has a relationship to the Todo model, the bacref is similar to adding 
    #another column, the lazy argument defines when sql alchemy loads the data, we can use it get the 
    #individual data for this user
    

    def __repr__(self):#how our object is printed whenever its printed out
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# create model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Text, nullable=False)
    duedate= db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#each task needs a user

    def __repr__(self):
        return f"User('{self.task}', '{self.duedate}')"