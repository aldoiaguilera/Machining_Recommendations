from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Manufacturer:
    DB = 'machining_recommendations'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
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
            manufacturers.append( cls(manufacturer) )
        return manufacturers
    
