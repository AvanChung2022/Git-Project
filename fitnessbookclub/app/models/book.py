from app.config.mysqlconnection import connectToMySQL
from app.models import user
from flask import flash

db = "fitnessbookclub"
class Book:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.description = db_data['description']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM books
                JOIN users on books.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        books = []
        for row in results:
            this_book = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_book.creator = user.User(user_data)
            books.append(this_book)
        return books
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM books
                JOIN users on books.user_id = users.id
                WHERE books.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_book = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_book.creator = user.User(user_data)
        return this_book

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO books (title,description,user_id)
                VALUES (%(title)s,%(description)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)

    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE books
                SET title = %(title)s,
                description = %(description)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM books
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_book(form_data):
        is_valid = True

        if len(form_data['title']) < 3:
            flash("Title must be at least 3 characters long.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False

        return is_valid