from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    DB = 'machining_recommendations'
    def __init__( self , data ):
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Input: Nothing
    # Output: List of class objects with user information
    @classmethod
    def get_all_users(cls):
        query = """
        SELECT * 
        FROM users
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    
    # Input: Email address
    # Output: Class object with user information
    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    # Input: Username
    # Output: Class object with user information
    @classmethod
    def get_user_by_username(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE username = %(username)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_by_user_id(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    # Input: User information
    # Output: User id
    @classmethod
    def save_user(cls, data ):
        query = """
        INSERT INTO users (username, first_name, last_name, email, password)
        VALUES (%(username)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    @classmethod
    def update_user_data(cls, data):
        query = """
        UPDATE users
        SET username = %(username)s, 
        last_name = %(last_name)s, 
        email = %(email)s
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    # Input: User information
    # Output: Boolean of whether or not user information is valid
    @staticmethod
    def validate_user_register(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'register_error')
            is_valid = False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters!", 'register_error')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters!", 'register_error')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long!", 'register_error')
            is_valid = False
        if User.get_user_by_email(data):
            flash("Email address is already in use!", 'register_error')
            is_valid = False
        if User.get_user_by_username(data):
            flash("That username is already in use!", 'register_error')
            is_valid = False
        return is_valid

    # Input: Unparsed registration data
    # Output: Parsed registration data
    @staticmethod
    def parse_user_register(data):
        parsed_data = {
            'username' : data['username'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': data['password']
        }
        return parsed_data

    # Input: Unparsed login data
    # Output: Parsed login data
    @staticmethod
    def parse_user_login(data):
        parsed_data = {
            'email': data['email'],
            'password': data['password']
        }
        return parsed_data

    @staticmethod
    def parse_user_update_data(data):
        parsed_data = {
            'id' : data['id'],
            'username' : data['username'],
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email']
        }
        return parsed_data

    @staticmethod
    def validate_user_update_data(new_data, old_data):
        is_valid = True
        if User.get_user_by_username(new_data) and old_data.username != new_data['username']:
            flash('Username is already in use!', 'update_error')
            is_valid = False
        if len(new_data['username']) < 3:
            flash('Username must be at least 3 characters long!', 'update_error')
            is_valid = False
        if not EMAIL_REGEX.match(new_data['email']): 
            flash("Invalid email address!", 'update_error')
            is_valid = False
        if len(new_data['first_name']) < 3:
            flash("First name must be at least 3 characters!", 'update_error')
            is_valid = False
        if len(new_data['last_name']) < 3:
            flash("Last name must be at least 3 characters!", 'update_error')
            is_valid = False
        if User.get_user_by_email(new_data) and old_data.email != new_data['email']:
            flash("Email address is already in use!", 'update_error')
            is_valid = False
        return is_valid
