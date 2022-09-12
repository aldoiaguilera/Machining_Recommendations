from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify

# Import classes
from flask_app.models.material import Material
from flask_app.models.recommendation import Recommendation

# Prepoluate tool page with information about tool and recommendations users have made
@app.route('/find/<material_id>')
def find(material_id):
    if 'user_id' not in session:
        return redirect('/')
    material = {'id': material_id}
    recommendations = {'material_id': material_id}
    material_found = Material.get_material_by_id(material)
    recommendations_found = Recommendation.get_recommendations_by_material_id(recommendations)
    return render_template('find.html', material=material_found, recommendations=recommendations_found)

# Retrieve materials based on insert to dynamically populate search form
@app.route('/get_materials/<insrt_id>')
def get_materials(insrt_id):
    data = {
        'insrt_id': insrt_id
    }
    return jsonify(Material.get_all_materials_by_insert_json(data))