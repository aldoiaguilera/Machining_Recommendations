from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Material:
    DB = 'machining_recommendations'
    def __init__( self , data ):
        self.id = data['id']
        self.material = data['material']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.insrt_id = data['insrt_id']
        self.information = []

    # Input: Insert id
    # Output: List of material information, not as an object
    @classmethod
    def get_all_materials_by_insert_json(cls, data):
        query = """
        SELECT * 
        FROM materials
        WHERE insrt_id = %(insrt_id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        materials = []
        for material in results:
            materials.append(material)
        return materials
    
    # Input: Material name
    # Output: Class object with material information
    @classmethod
    def get_material_by_name(cls, data):
        query = """
        SELECT * 
        FROM materials
        WHERE material = %(material)s
        ;"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])
    
    # Input: Material id
    # Output: Class object with material, manufacturer, and insert information
    @classmethod
    def get_material_by_id(cls, data):
        query = """
        SELECT * 
        FROM materials
        JOIN insrts
        ON insrts.id = materials.insrt_id
        JOIN manufacturers
        ON manufacturers.id = insrts.manufacturer_id
        WHERE materials.id = %(id)s;
        ;"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        material = cls(result[0])
        material.information.append(result[0]['manufacturer'])
        material.information.append(result[0]['insrt'])
        return material

    # Input: Material information
    # Output: Material id
    @classmethod
    def save_material(cls, data):
        search = Material.get_material_by_name(data)
        if search:
            return search.id
        query = """
        INSERT INTO materials (material, insrt_id)
        VALUES (%(material)s, %(insrt_id)s)
        ;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # Input: Material information 
    # Output: Boolean of whether or not material information is valid
    @staticmethod
    def validate_material_data(data):
        is_valid = True
        if len(data['material']) < 2:
            flash('Material must be at least 2 characters long', 'new_category_error')
            is_valid = False
        return is_valid