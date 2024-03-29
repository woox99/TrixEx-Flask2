from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 


# email format
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# only letters for name
NAME_REGEX = re.compile(r"^[a-zA-Z]+$") 
# Only letters and numbers for username
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9]+$") 


db = 'trixex'

class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.is_admin = db_data['is_admin']
        self.is_authorized = db_data['is_authorized']
        self.is_banned = db_data['is_banned']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.username = db_data['username']
        self.email = db_data['email']
        self.password = db_data['password']
        self.last_login = db_data['password']
        self.created_at = db_data['created_at']    
        self.updated_at = db_data['updated_at']   

    # GET USER ________________________
    @classmethod
    def get_all(cls):
            query = "SELECT * FROM users;"
            results = connectToMySQL(db).query_db(query)
            all_users = []
            for result in results:
                all_users.append(cls(result))
            return all_users

    @classmethod
    def get_all_formatted_date(cls):
            query = '''
            SELECT *, 
            DATE_FORMAT(last_login, '%b %d %Y %h:%i%p') 
            AS formatted_last_login 
            FROM users
            ORDER BY email ASC;
            '''
            results = connectToMySQL(db).query_db(query)
            return results
    
    @classmethod
    def get_user_by_id(cls, data):
        query = '''
        SELECT * FROM users
        WHERE users.id = %(userID)s;
        '''
        results = connectToMySQL(db).query_db(query,data)
        user = cls(results[0])
        return user
    
    @classmethod
    def get_user_by_email(cls,data):
            query = '''
            SELECT * FROM users
            WHERE email = %(email)s;
            '''
            results = connectToMySQL(db).query_db(query,data)
            if len(results) < 1:
                return False
            user = cls(results[0])
            return user
    
    @staticmethod
    def get_search_results(data):
        query = '''
            SELECT *
            FROM users
            WHERE users.username LIKE %(searchKey)s
                OR users.first_name LIKE %(searchKey)s
                OR users.last_name LIKE %(searchKey)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results

    # CREATE USER ________________________
    @staticmethod
    def create(data):
            query = '''
            INSERT INTO users
            (is_admin, is_authorized, is_banned, first_name, last_name, username, email, password, created_at, updated_at)
            VALUES ( 0, 0, 0, %(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s, NOW(), NOW()) 
            '''
            return connectToMySQL(db).query_db(query, data)
    
    # ADMIN ________________________
    @staticmethod
    def last_login(data):
        query = '''
        UPDATE users
        SET
            last_login = NOW()
        WHERE
            users.id = %(userID)s;
        '''
        return connectToMySQL(db).query_db(query, data)
    
    @staticmethod
    def authorize(data):
        query = '''
        UPDATE users
        SET
            is_authorized = %(is_authorized)s
        WHERE
            users.id = %(userID)s;
        '''
        return connectToMySQL(db).query_db(query, data)
    
    @staticmethod
    def ban(data):
        query = '''
        UPDATE users
        SET
            is_banned = %(is_banned)s
        WHERE
            users.id = %(userID)s;
        '''
        return connectToMySQL(db).query_db(query, data)
    
    @staticmethod
    def admin(data):
        query = '''
        UPDATE users
        SET
            is_admin = %(is_admin)s
        WHERE
            users.id = %(userID)s;
        '''
        return connectToMySQL(db).query_db(query, data)
    
    # VALIDATION _____________________________
    @staticmethod
    def validate_signup(user):
        existing_users = User.get_all()
        is_valid = True
        if len(user['first_name']) < 2:
            flash("Invalid first name.")
            is_valid = False
        if not NAME_REGEX.match(user['first_name']): 
            flash("Invalid first name. Must be letters only.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Invalid last name.")
            is_valid = False
        if not NAME_REGEX.match(user['last_name']): 
            flash("Invalid last name. Must be letters only.")
            is_valid = False
        if not USERNAME_REGEX.match(user['username']): 
            flash("Invalid username. Must be letters and numbers only.")
            is_valid = False
        for existing_user in existing_users:
            if user['username'] == existing_user.username:
                flash(f"{user['username']} is already taken.")
                is_valid = False   
            if user['email'] == existing_user.email:
                flash("This email is already associated with an account.")
                is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(data):
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email/password.")
            return False
        
        user = User.get_user_by_email(data)
        if not user:
            flash("Invalid email/password.")
            return False
        
        if not bcrypt.check_password_hash(user.password, data['password']):
            flash("Invalid email/password.")
            return False
        
        return user
