from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

# Import classes
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = User.parse_user_register(request.form)
    if not User.validate_user_register(data):
        return redirect('/')
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    pass
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')