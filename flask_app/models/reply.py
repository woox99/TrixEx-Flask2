from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# from flask_app import bcrypt

db = 'trixex'

class Reply:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.comment_id = db_data['comment_id']
        self.trick_id = db_data['trick_id']
        self.content = db_data['content']
        self.created_at = db_data['updated_at']    
        self.updated_at = db_data['updated_at']    

    @staticmethod
    def get_replies_by_trickID(data):
        query = '''
            SELECT replies.*, users.*, DATE_FORMAT(replies.created_at, '%%b %%d, %%Y') AS formatted_replies_created_at 
            FROM replies 
            JOIN users
            ON users.id = replies.user_id
            WHERE replies.trick_id = %(trickID)s
            ORDER BY replies.created_at DESC;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results
    
    @staticmethod
    def get_reply_and_creator(data):
        query = '''
            SELECT * FROM replies
            JOIN users
            ON users.id = replies.user_id
            WHERE replies.id = %(replyID)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results[0]
    
    # CREATE COMMENT___________________________________
    @staticmethod
    def create(data):
        query = '''
        INSERT INTO replies 
        (trick_id, comment_id, user_id, content, created_at, updated_at)
        VALUES( %(trickID)s, %(commentID)s, %(userID)s, %(content)s, NOW(), NOW());
        '''
        return connectToMySQL(db).query_db(query, data)
    
    # DELETE REPLY ______________________________________
    @staticmethod
    def delete_by_trickID(data):
        query = '''
        DELETE FROM replies
        WHERE replies.trick_id = %(trickID)s;
        '''
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def delete_by_replyID(data):
        query = '''
        DELETE FROM replies
        WHERE replies.id = %(replyID)s;
        '''
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def delete_by_commentID(data):
        query = '''
        DELETE FROM replies
        WHERE replies.comment_id = %(commentID)s;
        '''
        return connectToMySQL(db).query_db(query, data)