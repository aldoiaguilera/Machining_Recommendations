from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module

# Create class that matches database
class User:
    def __init__( self , data ):
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """
        SELECT * 
        FROM 
        ;"""
        results = connectToMySQL('').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
            
    @classmethod
    def save(cls, data ):
        query = """
        INSERT INTO  
        VALUES 
        ;"""
        return connectToMySQL('').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM users
        WHERE id = %(id)s
        ;"""
        return connectToMySQL('').query_db( query, data )

    @classmethod
    def update(cls, data):
        query = """
        UPDATE 
        SET 
        WHERE 
        ;"""
        return connectToMySQL('').query_db( query, data )

    @staticmethod
    def validate_user( user ):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

