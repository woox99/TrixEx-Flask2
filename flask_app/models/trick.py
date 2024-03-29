from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import urllib.parse

# from flask_app import bcrypt

db = 'trixex'

class Trick:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.name = db_data['name']
        self.html = db_data['html']
        self.css = db_data['css']
        self.js = db_data['js']
        self.scale = db_data['scale']
        self.description = db_data['description']
        self.is_private = db_data['is_private']
        self.num_views = db_data['num_views']
        self.created_at = db_data['created_at']    
        self.updated_at = db_data['updated_at']   

        self.creator = None # User class object will be assigned to this


    # CREATE TRICK ___________________________________________________________
    @staticmethod
    def create(data):
        query = '''
        INSERT INTO tricks 
        (user_id, name, html, css, js, scale, description, is_private, num_views, created_at, updated_at)
        VALUES( %(userID)s, %(trick_name)s, %(encoded_html)s, %(encoded_css)s, %(encoded_js)s, %(scale)s, %(description)s, %(is_private)s, %(num_views)s, NOW(), NOW());
        '''
        return connectToMySQL(db).query_db(query, data)

    # DELETE TRICK ___________________________________________________________
    @staticmethod
    def delete(data):
        query = '''
        DELETE FROM tricks
        WHERE tricks.id = %(trickID)s;
        '''
        return connectToMySQL(db).query_db(query, data)

    # UPDATE TRICK ___________________________________________________________
    @staticmethod
    def update(data):
        query = '''
        UPDATE tricks
        SET
            name = %(trick_name)s,
            html = %(encoded_html)s,
            css = %(encoded_css)s,
            js = %(encoded_js)s,
            scale = %(scale)s,
            description = %(description)s,
            is_private = %(is_private)s,
            updated_at = NOW()
        WHERE
            tricks.id = %(trickID)s;
        '''
        return connectToMySQL(db).query_db(query, data)

    # GET TRICK ___________________________________________________________
    @classmethod
    def get_trick_by_trickID(cls, data):
        query = '''
            SELECT * FROM tricks
            WHERE tricks.id = %(trickID)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        result = results[0]
        return cls(result)

    @classmethod
    def get_trick_and_creator_by_trickID(cls, data):
        query = '''
            SELECT * FROM tricks
            JOIN users
            ON users.id = tricks.user_id
            WHERE tricks.id = %(trickID)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results[0]

    @staticmethod
    def get_all_with_favorited_by_active_user(data):
        query = '''
            SELECT tricks.*, users.*, DATE_FORMAT(tricks.created_at, '%%b %%d, %%Y') AS formatted_trick_created_at,
            IF(favorites.user_id IS NOT NULL, 1, 0) AS favorited_by_active_user
            FROM tricks
            JOIN users ON users.id = tricks.user_id
            LEFT JOIN favorites ON tricks.id = favorites.trick_id AND favorites.user_id = %(userID)s
            ORDER BY tricks.created_at DESC;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results

    @staticmethod
    def get_all_favorited_by_active_user(data):
        query = '''
            SELECT tricks.*, users.*, DATE_FORMAT(tricks.created_at, '%%b %%d %%y') AS formatted_trick_created_at
            FROM tricks
            JOIN users ON users.id = tricks.user_id
            JOIN favorites ON tricks.id = favorites.trick_id AND favorites.user_id = %(userID)s
            ORDER BY tricks.created_at DESC;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results

    @staticmethod
    def get_all():
        query = '''
            SELECT tricks.*, users.*, DATE_FORMAT(tricks.created_at, '%b %d, %Y') AS formatted_trick_created_at 
            FROM tricks
            JOIN users ON users.id = tricks.user_id
            ORDER BY tricks.created_at DESC;
        '''
        results = connectToMySQL(db).query_db(query)
        return results

    @staticmethod
    def get_all_by_otherID(data):
        query = '''
            SELECT tricks.*, users.*, DATE_FORMAT(tricks.created_at, '%%b %%d, %%Y') AS formatted_trick_created_at,
            IF(favorites.user_id IS NOT NULL, 1, 0) AS favorited_by_active_user
            FROM tricks
            JOIN users ON users.id = tricks.user_id
            LEFT JOIN favorites ON tricks.id = favorites.trick_id AND favorites.user_id = %(userID)s
            WHERE tricks.user_id = %(otherID)s
            ORDER BY tricks.created_at DESC;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results

    @staticmethod
    def guest_get_all_by_otherID(data):
        query = '''
            SELECT tricks.*, users.*, DATE_FORMAT(tricks.created_at, '%%b %%d, %%Y') AS formatted_trick_created_at
            FROM tricks
            JOIN users ON users.id = tricks.user_id
            WHERE tricks.user_id = %(userID)s
            ORDER BY tricks.created_at DESC;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results

    @staticmethod
    def get_search_results(data):
        query = '''
            SELECT tricks.*, users.*, DATE_FORMAT(tricks.created_at, '%%b %%d, %%Y') AS formatted_trick_created_at
            FROM tricks
            JOIN users ON users.id = tricks.user_id
            WHERE tricks.name LIKE %(searchKey)s
                OR users.first_name LIKE %(searchKey)s
                OR users.last_name LIKE %(searchKey)s
                OR users.username LIKE %(searchKey)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        if len(results) == 0:
            return False
        return results
    
    @staticmethod
    def get_all_search_results_with_faved_by_actuser(data):
        query = '''
            SELECT tricks.*, users.*, DATE_FORMAT(tricks.created_at, '%%b %%d, %%Y') AS formatted_trick_created_at,
            IF(favorites.user_id IS NOT NULL, 1, 0) AS favorited_by_active_user
            FROM tricks
            JOIN users ON users.id = tricks.user_id
            LEFT JOIN favorites ON tricks.id = favorites.trick_id AND favorites.user_id = %(userID)s
            WHERE tricks.name LIKE %(searchKey)s
                OR users.first_name LIKE %(searchKey)s
                OR users.last_name LIKE %(searchKey)s
                OR users.username LIKE %(searchKey)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        if len(results) == 0:
            return False
        return results
    
    # ADD VIEWS ______________________________________
    @staticmethod
    def add_views(data):
        query = '''
        UPDATE tricks
        SET num_views = %(num_views)s
        WHERE tricks.id = %(trickID)s;
        '''
        return connectToMySQL(db).query_db(query, data)
    
    # VALIDATE TRICK _________________________________
    @staticmethod
    def validate_trick(trick):
        is_valid = True
        if trick['is_authorized'] == 0:
            flash('SORRY! Only authorized users can upload tricks. If you you would like to become authorized, please send me a request.')
            is_valid = False
        existing_tricks = Trick.get_all()
        for existing_trick in existing_tricks:
            if trick['trick_name'] == existing_trick['name']:
                flash("That name is already taken.")
                is_valid = False
            if trick['encoded_html'] == existing_trick['html'] \
                and trick['encoded_css'] == existing_trick['css'] \
                    and trick['encoded_js'] == existing_trick['js']:
                flash("That trick has already been created by another user. Please only upload original content.")
                is_valid = False
        return is_valid
    
