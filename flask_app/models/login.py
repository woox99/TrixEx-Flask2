from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 


db = 'trixex'

class Login:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']    

    # CREATE LOGIN ________________________
    @staticmethod
    def login_stamp(data):
            query = '''
            INSERT INTO logins
            (user_id) VALUES (%(userID)s);
            '''
            results = connectToMySQL(db).query_db(query,data)
            return results
    
    @staticmethod
    def get_all_formatted_date():
            query = '''
            SELECT *, 
            DATE_FORMAT(logins.created_at, '%b %d %Y %h:%i%p') 
            AS formatted_created_at 
            FROM logins
            JOIN users
            ON users.id = logins.user_id
            ORDER BY logins.created_at DESC;
            '''
            results = connectToMySQL(db).query_db(query)
            return results


