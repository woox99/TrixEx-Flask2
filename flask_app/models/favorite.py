from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# from flask_app import bcrypt

db = 'trixex'

class Favorite:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.trick_id = db_data['trick_id']
        self.created_at = db_data['updated_at']    
        self.updated_at = db_data['updated_at']  

    @staticmethod
    def create(data):
            query = '''
            INSERT IGNORE INTO favorites
            (user_id, trick_id, created_at, updated_at)
            SELECT %(userID)s, %(trickID)s, NOW(), NOW()
            FROM dual
            WHERE NOT EXISTS (
                SELECT 1
                FROM favorites
                WHERE user_id = %(userID)s AND trick_id = %(trickID)s);
            '''
            return connectToMySQL(db).query_db(query, data)
    
    # DELETE FAVORITE ___________________________________________________________
    @staticmethod
    def delete_favorite(data):
        query = '''
        DELETE
        FROM favorites
        WHERE favorites.trick_id = %(trickID)s;
        '''
        return connectToMySQL(db).query_db(query, data)

    # GET FAVORITE ______________________________________
    @staticmethod
    def get_favorites_by_userID(data):
            query = '''
            SELECT * FROM favorites
            WHERE favorites.user_id = %(userID)s;
            '''
            return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def get_favorite(data):
            query = '''
            SELECT *
            FROM favorites
            WHERE favorites.user_id = %(userID)s AND favorites.trick_id = %(trickID)s;
            '''
            result = connectToMySQL(db).query_db(query, data)
            if not result:
                return False
            return True

    # DELETE FAVORITE ___________________________
    @staticmethod
    def delete(data):
            query = '''
            DELETE FROM favorites
            WHERE favorites.user_id = %(userID)s AND favorites.trick_id = %(trickID)s;
            '''
            return connectToMySQL(db).query_db(query, data)