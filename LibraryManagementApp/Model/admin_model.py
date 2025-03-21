from Model.user_model import User
from Model.book_model import Book
from Database.db_lma import Database

class Admin(User): # Include all the ADMIN ONLY function
    def __init__(self, user_id=None, name=None, username=None, email=None, password=None, date_of_birth=None, database=None):
        super().__init__(user_id, name, username, email, password, date_of_birth, role="admin")
        self.db = Database()  # Connect to database

    def add_user(new_user): # Add new user 
        """Don't need to check if the user is already existed, because the user_id is distinguished"""
        new_user.save_user()
    
    def reset_password(self, user_id): #Reset account password to default password
        if not User.get_id(user_id):
            return False # User not found
        default_password = "123456789"
        self.db.cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (default_password, user_id))
        self.db.conn.commit()
        return True 

    def delete_user(self, user_id): #Delete user
        """
        Removes a user from the users table based on the given user_id.
        """
        try:
            # Ensure user_id is an integer
            user_id = int(user_id)
            if not User.get_id(user_id):
                return False # User not found
            self.db.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            self.db.conn.commit()
            # Verify deletion
            if self.db.cursor.rowcount > 0:
                print(f"User with ID {user_id} successfully deleted")
                return True
            else:
                print(f"No rows affected when deleting user {user_id}")
                return False
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    
    def add_book(self, book_id, title, author, category, published_year, quantity): # Add new book
        if Book.get_book_by_id(book_id):
            return False # Book already exists
        book = Book(book_id, title, author, category, published_year, quantity)
        book.save_book()
        return True
    
    def edit_book(self, book_id, new_data): # Edit books
        book_data = Book.get_book_by_id(book_id)  # This returns a tuple
        if book_data:
            book = Book(*book_data)  # Convert tuple to Book object
            book.update_book(new_data) # Update the book
            return True
        return False # Book not found
       
    # def delete_book(self, book_id):
    #     if not Book.get_book_by_id(book_id):
    #         return False # Book not found
    #     self.db.cursor.execute("DELETE FROM Books WHERE book_id = ?", (book_id,))
    #     self.db.conn.commit()
    #     return True
    def delete_book(self, book_id):
        # Don't convert book_id to int, keep it as string to preserve leading zeros
        if not Book.get_book_by_id(book_id):
            return False  # Book not found
        self.db.cursor.execute("DELETE FROM Books WHERE book_id = ? ", (book_id,))
        self.db.conn.commit()
        return True
