from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# from flask_app import bcrypt

db = 'trixex'

class Comment:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.trick_id = db_data['trick_id']
        self.content = db_data['content']
        self.created_at = db_data['updated_at']    
        self.updated_at = db_data['updated_at'] 

    # GET COMMENT___________________________________
    @staticmethod
    def get_comments_by_trickID(data):
        query = '''
            SELECT comments.*, users.*, DATE_FORMAT(comments.created_at, '%%b %%d, %%Y') AS formatted_comment_created_at 
            FROM comments 
            JOIN users
            ON users.id = comments.user_id
            WHERE comments.trick_id = %(trickID)s
            ORDER BY comments.created_at DESC;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results
    
    @staticmethod
    def get_comment_and_creator(data):
        query = '''
            SELECT * FROM comments
            JOIN users
            ON users.id = comments.user_id
            WHERE comments.id = %(commentID)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results[0]
    
    
    # CREATE COMMENT___________________________________
    @staticmethod
    def create(data):
        query = '''
        INSERT INTO comments 
        (trick_id, user_id, content, created_at, updated_at)
        VALUES( %(trickID)s, %(userID)s, %(content)s, NOW(), NOW());
        '''
        return connectToMySQL(db).query_db(query, data)

    # DELETE COMMENT___________________________________
    @staticmethod
    def delete(data):
        query = '''
        DELETE FROM comments
        WHERE comments.id = %(commentID)s;
        '''
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def delete_by_trickID(data):
        query = '''
        DELETE FROM comments
        WHERE comments.trick_id = %(trickID)s;
        '''
        return connectToMySQL(db).query_db(query, data)
