from operator import attrgetter
from flask import request, render_template, url_for, redirect, session, flash, jsonify
from todoapp import app, db, bcrypt
from todoapp.models import Todo, User
from todoapp.forms import RegistrationForm, LoginForm, TaskForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@login_required
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    form = TaskForm()
    sorttasks = Todo.query.all()
    form = TaskForm()
    
    return render_template('index.html', incomplete=incomplete, complete=complete, form=form, sorttasks=sorttasks)

#User system
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in.', 'success')
            return redirect(url_for('login', user=user))
        except:
            flash('There was an issue creating your account. Please try again.', 'danger')
    else:    
        return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title='Account')


#Task Functionality
@app.route('/task/', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    task = Todo(task=form.task.data, duedate=form.duedate.data, complete=False)
    if form.validate_on_submit():   
        try:
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            flash('There was an issue adding your task', 'danger')
    else:
        return render_template('index.html', title='index', form=form)
    
@app.route('/complete/<id>')
@login_required
def complete(id):
    #first becuase we are only expecting one item from the database back
    task = Todo.query.filter_by(id=int(id)).first()
    task.complete = True
    
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/incomplete/<id>')
@login_required
def incomplete(id):
    
    task = Todo.query.filter_by(id=int(id)).first()
    task.complete = False
    
    db.session.commit()

    
    return redirect(url_for('index'))

@app.route('/delete/<id>')
@login_required
def delete(id):
    task = Todo.query.filter_by(id=int(id)).one()
    task.complete = True
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
@login_required
def update(id):
    updatetask = Todo.query.get_or_404(id)
    form = TaskForm()
    if request.method == 'POST' and form.validate_on_submit: 
        updatetask.task = request.form['task']
        #updatetask.duedate = request.form['duedate']
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('index', id=id))
    elif request.method == 'GET':
        form.task.data = updatetask.task
        form.duedate.data = updatetask.duedate
    return render_template('update.html', title='Update Task', updatetask=updatetask, form=form)

@app.route('/sort', methods=['GET','POST'])
def sort():
    sorttasks = Todo.query.all()
    form = TaskForm()
    
    sorted(sorttasks, key=attrgetter('duedate'))
    #sorted(sorttasks, key=lambda sorttasks: sorttasks.duedate)
    db.session.commit()
    flash('Your task has been sorted!', 'success')
         
    return redirect(url_for('index', sorttasks=sorttasks))
    

@app.route("/about")
def about():

    return render_template('about.html')