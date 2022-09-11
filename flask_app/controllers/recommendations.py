from flask_app import app
from flask import render_template, redirect, request, session, flash

# Import classes
from flask_app.models.recommendation import Recommendation

@app.route('/add_recommendation', methods=['POST'])
def add_recommendation():
    if request.form['velocity'] == '' or request.form['feed'] == '' or request.form['depth_of_cut'] == '':
        flash('Do not leave any box empty', 'recommendation_error')
        return redirect(f'/find/' + request.form['material_id'])
    recommendation = Recommendation.parse_recommendation_data(request.form)
    if not Recommendation.validate_recommendation(recommendation):
        return redirect(f'/find/' + recommendation['material_id'])
    Recommendation.save_recommendation(recommendation)
    return redirect(f'/find/' + recommendation['material_id'])

@app.route('/edit/<recommendation_id>')
def edit_recommendation(recommendation_id):
    data = { 'recommendation_id': recommendation_id}
    recommendation = Recommendation.get_recommendation_by_recommendation_id(data)
    if session['user_id'] != recommendation.user_id:
        return redirect('/dashboard')
    return render_template('edit_recommendation.html', recommendation=recommendation)

@app.route('/update_recommendation', methods=['POST'])
def update_recommendation():
    if request.form['velocity'] == '' or request.form['feed'] == '' or request.form['depth_of_cut'] == '':
        flash('Do not leave any box empty', 'recommendation_error')
        return redirect('/edit/' + request.form['material_id'])
    recommendation = Recommendation.parse_recommendation_data(request.form)
    recommendation['id'] = request.form['id']
    if not Recommendation.validate_recommendation(recommendation):
        return redirect('/edit/' + recommendation.material_id)
    Recommendation.update_recommendation(recommendation)
    return redirect('/find/' + str(recommendation['material_id']))

@app.route('/delete/<recommendation_id>')
def delete_recommendation(recommendation_id):
    data = { 'id': recommendation_id, 'recommendation_id': recommendation_id}
    recommendation = Recommendation.get_recommendation_by_recommendation_id(data)
    if session['user_id'] != recommendation.user_id:
        return redirect('/dashboard')
    Recommendation.delete_recommendation(data)
    return redirect('/find/' + str(recommendation.material_id))