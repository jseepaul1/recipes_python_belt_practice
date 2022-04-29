from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


class Recipe:
    def __init__(self, recipe_data):
        self.id = recipe_data['id']
        self.name = recipe_data['name']
        self.description = recipe_data['description']
        self.under_30_minutes = recipe_data['under_30_minutes']
        self.instructions = recipe_data['instructions']
        self.date_made = recipe_data['date_made']
        self.user_id = recipe_data['user_id']
        self.created_at = recipe_data['created_at']
        self.updated_at = recipe_data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name,description,under_30_minutes,instructions,date_made, user_id) VALUES (%(name)s,%(description)s,%(under_30_minutes)s,%(instructions)s,%(date_made)s,%(user_id)s);"
        return connectToMySQL('recipe').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"

        recipe_results = connectToMySQL("recipe").query_db(
            query
        )
        recipes = []
        for recipe in recipe_results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        recipe_from_db = connectToMySQL('recipe').query_db(query, data)
        print('result_from_db - ', recipe_from_db)
        return cls(recipe_from_db[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30_minutes=%(under_30_minutes)s, date_made=%(date_made)s WHERE id = %(id)s;"
        return connectToMySQL('recipe').query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipe').query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters!", "recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters!", "recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters!", "recipe")
        if recipe['date_made'] == "":
            is_valid = False
            flash("Date is required to complete the form!", "recipe")
        return is_valid

    @classmethod
    def get_recipes_by_user_id(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE users.id = %(id)s;"
        recipe_results = connectToMySQL('recipe').query_db(query, data)
        recipes = []
        for row in recipe_results:
            print('row - ', row)
            recipe_data = {
                "id": row['id'],
                "name": row['name'],
                "description": row['description'],
                "instructions": row['instructions'],
                "date_made": row['date_made'],
                "under_30_minutes": row['under_30_minutes'],
                "user_id": row['user_id'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            recipes.append(Recipe(recipe_data))
        return recipes
