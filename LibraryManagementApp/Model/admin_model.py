from Model.user_model import User
from Model.book_model import Book
from Database.db_lma import Database

class Admin(User):
    def __init__(self, user_id=None, name=None, username=None, email=None, password=None, date_of_birth=None, database=None):
        super().__init__(user_id, name, username, email, password, date_of_birth, role="admin")
        self.db = database  # Kết nối database

    def add_user(new_user):
        new_user.save_user()
    
    def reset_password(self, user_id):
        default_password = "123456789"
        self.db.cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (default_password, user_id))
        self.db.conn.commit()

    def delete_user(self, user_id):
        self.db.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        self.db.conn.commit()
    
    def add_book(self, title, author, category, published_year, quantity):
        book = Book(title, author, category, published_year, quantity)
        book.save_book()
    
    def edit_book(self, book_id, new_data):
        book = Book.get_book_by_id(book_id)
        if book:
            book.update_book(new_data)
            return "Updated Successfully"
        return None
       
    def delete_book(self, book_id):
        self.db.cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        self.db.conn.commit()