from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify

# Import classes
from flask_app.models.material import Material

@app.route('/get_materials/<insrt_id>')
def get_materials(insrt_id):
    data = {
        'insrt_id': insrt_id
    }
    return jsonify(Material.get_all_materials_by_insert_json(data))