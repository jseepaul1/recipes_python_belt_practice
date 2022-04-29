from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, user_data):
        self.id = user_data['id']
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.email = user_data['email']
        self.password = user_data['password']
        self.created_at = user_data['created_at']
        self.updated_at = user_data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        user_results = connectToMySQL("recipe").query_db(
            query
        )
        users = []
        for user in user_results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s);"
        return connectToMySQL("recipe").query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        # print('data - ', data)
        query = "SELECT * FROM users WHERE id = %(id)s"
        result_from_db = connectToMySQL("recipe").query_db(query, data)
        # print('result_from_db - ', result_from_db)
        return cls(result_from_db[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("recipe").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("recipe").query_db(query, user)
        print('user -', user)
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First Name must be at least 2 characters!", "registration")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 2 characters!", "registration")
            is_valid = False
        if len(results) >= 1:
            flash("Email already taken!", "registration")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address!", "registration")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters to register!",
                  "registration")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Sorry password does not match!", "registration")
            is_valid = False
        return is_valid
