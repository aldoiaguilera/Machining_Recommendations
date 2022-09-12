from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify

# Import classes
from flask_app.models.insert import Insert

# Retrieve inserts based on manufacturer to dynamically populate search form
@app.route('/get_inserts/<manufacturer_id>')
def get_inserts(manufacturer_id):
    data = {
        'manufacturer_id': manufacturer_id
    }
    return jsonify(Insert.get_inserts_by_manufacturer_json(data))
