from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify

# Import classes
from flask_app.models.manufacturer import Manufacturer

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    manufacturers = Manufacturer.get_all_manufacturers()
    return render_template('dashboard.html', manufacturers=manufacturers)

@app.route('/get_data')
def get_data():
    return Manufacturer.get_all_manufacturers()
