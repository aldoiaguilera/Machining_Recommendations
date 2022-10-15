from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Import classes
from flask_app.models.user import User

# Default login / Registration page
@app.route('/')
def index():
    return render_template('index.html')

# Validates user registration data
# Signs user in and sends them to dashboard if successful
@app.route('/register', methods=['POST'])
def register():
    if request.form['confirm_password'] != request.form['password']:
        flash("Passwords do not match!", 'register_error')
        return redirect('/')
    data = User.parse_user_register(request.form)
    if not User.validate_user_register(data):
        return redirect('/')
    data['password'] = bcrypt.generate_password_hash(data['password'])
    session['user_id'] = User.save_user(data)
    session['username'] = data['username']
    return redirect('/dashboard')

# Validates user login data with database
# Signs user in and sends them to dashboard if successful
@app.route('/login', methods=['POST'])
def login():
    data = User.parse_user_login(request.form)
    user = User.get_user_by_email(data)
    if not user:
        flash('Invalid email address', 'login_error')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, data['password']):
        flash('Invalid password', 'login_error')
        return redirect('/')
    session['user_id'] = user.id
    session['username'] = user.username
    return redirect('/dashboard')

# Logs user out and returns them to login/registration page
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect('/')
    data = { 'id' : session['user_id'] }
    user = User.get_user_by_user_id(data)
    return render_template('account.html', user=user)

@app.route('/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/')
    new_data = User.parse_user_update_data(request.form)
    old_data = User.get_user_by_user_id(new_data)
    if not User.validate_user_update_data(new_data, old_data):
        return redirect('/account')
    User.update_user_data(new_data)
    session['username'] = new_data['username']
    return redirect('/account')