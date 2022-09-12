from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Insert:
    DB = 'machining_recommendations'
    def __init__( self , data ):
        self.id = data['id']
        self.insrt = data['insrt']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.manufacturer_id = data['manufacturer_id']
    
    # Input: manufacturer_id
    # Output: List of insert information, not as object
    @classmethod
    def get_inserts_by_manufacturer_json(cls, data):
        query = """
        SELECT *
        FROM insrts
        WHERE manufacturer_id = %(manufacturer_id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        insrts = []
        for insrt in results:
            insrts.append(insrt)
        return insrts
    
    # Input: insert name
    # Output: Class object with insert information
    @classmethod
    def get_insert_by_name(cls, data):
        query = """
        SELECT * 
        FROM insrts
        WHERE insrt = %(insrt)s
        ;"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    # Input: Insert information
    # Output: Insert id
    @classmethod
    def save_insert(cls, data):
        search = Insert.get_insert_by_name(data)
        if search:
            return search.id
        query = """
        INSERT INTO insrts (insrt, manufacturer_id)
        VALUES (%(insrt)s, %(manufacturer_id)s)
        ;"""
        return connectToMySQL(cls.DB).query_db(query, data)

    # Input: Insert information 
    # Output: Boolean of whether or not insert information is valid
    @staticmethod
    def validate_insert_data(data):
        is_valid = True
        if len(data['insrt']) < 2:
            flash('Insert must be at least 2 characters long', 'new_category_error')
            is_valid = False
        return is_valid