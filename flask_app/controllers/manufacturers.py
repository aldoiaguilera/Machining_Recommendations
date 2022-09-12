from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify

# Import classes
from flask_app.models.manufacturer import Manufacturer
from flask_app.models.insert import Insert
from flask_app.models.material import Material

# Prepopulate dashboard with available manufacturers
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    manufacturers = Manufacturer.get_all_manufacturers()
    return render_template('dashboard.html', manufacturers=manufacturers)

# Parse, validate, and save manufacturer, insert, and material information (if not already in database)
@app.route('/add_new_category', methods=['POST'])
def add_new_category():
    # Parse form data
    data = {
        'manufacturer': request.form['manufacturer'],
        'insrt' : request.form['insrt'],
        'material' : request.form['material']
    }

    # Validate form data
    if not Manufacturer.validate_manufacturer_data(data) or not Insert.validate_insert_data(data) or not Material.validate_material_data(data):
        return redirect('/dashboard')

    # Save form data
    data['manufacturer_id'] = Manufacturer.save_manufacturer(data)
    data['insrt_id'] = Insert.save_insert(data)
    Material.save_material(data)

    return redirect('/dashboard')