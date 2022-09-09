from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Manufacturer:
    DB = 'machining_recommendations'
    def __init__( self , data ):
        self.id = data['id']
        self.manufacturer = data['manufacturer']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_manufacturers(cls):
        query = """
        SELECT * 
        FROM manufacturers
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        manufacturers = []
        for manufacturer in results:
            manufacturers.append(manufacturer)
        return manufacturers
    
    @classmethod
    def get_manufacturer_by_name(cls, data):
        query = """
        SELECT * 
        FROM manufacturers
        WHERE manufacturer = %(manufacturer)s
        ;"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def save_manufacturer(cls, data):
        search = Manufacturer.get_manufacturer_by_name(data)
        if search:
            return search.id
        query = """
        INSERT INTO manufacturers (manufacturer)
        VALUES (%(manufacturer)s)
        ;"""
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_manufacturer_data(data):
        is_valid = True
        if len(data['manufacturer']) < 2:
            flash('Manufacturer must be at least 2 characters long', 'new_category_error')
            is_valid = False
        return is_valid