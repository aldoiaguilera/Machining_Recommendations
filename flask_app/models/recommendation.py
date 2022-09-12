from asyncio.windows_events import NULL
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recommendation:
    DB = 'machining_recommendations'
    def __init__( self , data ):
        self.id = data['id']
        self.velocity = data['velocity']
        self.feed = data['feed']
        self.depth_of_cut = data['depth_of_cut']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.material_id = data['material_id']
        self.user_id = data['user_id']
        self.other = None
    
    # Input: Material id
    # Output: List of Class objects with recommendation information
    @classmethod
    def get_recommendations_by_material_id(cls, data):
        query = """
        SELECT *
        FROM recommendations
        JOIN users 
        ON recommendations.user_id = users.id
        WHERE material_id = %(material_id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        recommendations = []
        for recommendation in results:
            recommendations.append(cls(recommendation))
        for i in range(0, len(recommendations)):
            data = { 'username': results[i]['username']}
            recommendations[i].other = data
        return recommendations

    # Input: Recommendation id
    # Output: Class object with recommendation information
    @classmethod
    def get_recommendation_by_recommendation_id(cls, data):
        query = """
        SELECT *
        FROM recommendations
        JOIN users 
        ON recommendations.user_id = users.id
        JOIN materials
        ON recommendations.material_id = materials.id
        JOIN insrts
        ON materials.insrt_id = insrts.id
        JOIN manufacturers
        ON insrts.manufacturer_id = manufacturers.id
        WHERE recommendations.id = %(recommendation_id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        recommendation = []
        recommendation.append(cls(results[0]))
        data = {
            'manufacturer': results[0]['manufacturer'],
            'insrt' : results[0]['insrt'],
            'material' : results[0]['material'],
            'material_id' : results[0]['materials.id']
        }
        recommendation[0].other = data
        return recommendation[0]

    # Input: Recommendation information
    # Output: Recommendation id
    @classmethod
    def save_recommendation(cls, data ):
        query = """
        INSERT INTO recommendations (velocity, feed, depth_of_cut, material_id, user_id)
        VALUES (%(velocity)s, %(feed)s, %(depth_of_cut)s, %(material_id)s, %(user_id)s)
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    # Input: Recommendation information
    # Output: Nothing
    @classmethod
    def update_recommendation(cls, data ):
        query = """
        UPDATE recommendations
        SET velocity = %(velocity)s,
        feed = %(feed)s,
        depth_of_cut = %(depth_of_cut)s
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )
    
    # Input: Recommendation id
    # Output: Nothing
    @classmethod
    def delete_recommendation(cls, data ):
        query = """
        DELETE FROM recommendations
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    # Input: Recommendation information
    # Output: Boolean of whether or not recommendation information is valid
    @staticmethod
    def validate_recommendation(data):
        is_valid = True
        if data['velocity'] < 1 or data['velocity'] > 2000:
            flash("Velocity must be between 1 and 2000", 'recommendation_error')
            is_valid = False
        if float(data['feed']) < 0.001 or float(data['feed']) > 0.030:
            flash("Feed must be between .001 and 0.030", 'recommendation_error')
            is_valid = False
        if float(data['depth_of_cut']) < 0.01 or float(data['depth_of_cut']) > 0.300:
            flash("Depth of cut must be between 0.01 and 0.300", 'recommendation_error')
            is_valid = False
        return is_valid

    # Input: Unparsed recommendation data
    # Output: Parsed recommendation data
    @staticmethod
    def parse_recommendation_data(data):
        parsed_data = {
            'velocity' : int(data['velocity']),
            'feed': data['feed'],
            'depth_of_cut': data['depth_of_cut'],
            'material_id': data['material_id'],
            'user_id' : data['user_id']
        }
        return parsed_data