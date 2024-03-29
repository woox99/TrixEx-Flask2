from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# from flask_app import bcrypt

db = 'trixex'

class Follower:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.follower_id = db_data['follower_id']
        self.following_id = db_data['following_id']
        self.created_at = db_data['updated_at']    
        self.updated_at = db_data['updated_at']    

    # GET FOLLOWERS _____________________________________
    @classmethod
    def get_all_followers_by_userID(cls, data):
        query = '''
        SELECT * 
        FROM followers
        JOIN users
        ON users.id = followers.follower_id
        WHERE followers.following_id = %(userID)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_all_followings_by_userID(cls, data):
        query = '''
        SELECT * 
        FROM followers
        JOIN users
        ON users.id = followers.following_id
        WHERE followers.follower_id = %(userID)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_all_by_userID(cls, data):
        query = '''
        SELECT * 
        FROM followers
        JOIN users
        ON users.id = followers.follower_id
        WHERE followers.following_id = %(userID)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results
    
    @staticmethod
    def get_follow(data):
            query = '''
            SELECT *
            FROM followers
            WHERE followers.follower_id = %(userID)s AND followers.following_id = %(otherID)s;
            '''
            result = connectToMySQL(db).query_db(query, data)
            if not result:
                return False
            return True

    @staticmethod
    def get_follower_count(data):
        query = '''
        SELECT COUNT(*) AS num_followers
        FROM followers
        WHERE followers.following_id = %(otherID)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results[0]

    @staticmethod
    def get_following_count(data):
        query = '''
        SELECT COUNT(*) AS num_followings
        FROM followers
        WHERE followers.follower_id = %(otherID)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return results[0]
    
    # CREATE FOLLOWER _______________________________________
    @staticmethod
    def create(data):
            query = '''
            INSERT IGNORE INTO followers
            (follower_id, following_id, created_at, updated_at)
            SELECT %(userID)s, %(otherID)s, NOW(), NOW()
            FROM dual
            WHERE NOT EXISTS (
                SELECT 1
                FROM followers
                WHERE follower_id = %(userID)s AND following_id = %(otherID)s);
            '''
            return connectToMySQL(db).query_db(query, data)
    
    # DELETE FOLLOWER _______________________________
    @staticmethod
    def delete(data):
            query = '''
            DELETE FROM followers
            WHERE followers.follower_id = %(userID)s AND followers.following_id = %(otherID)s;
            '''
            return connectToMySQL(db).query_db(query, data)
