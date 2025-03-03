from Model.user_model import User
from Model.book_model import Book
from Database.db_lma import Database

class Admin(User):
    def __init__(self, user_id=None, name=None, username=None, email=None, password=None, date_of_birth=None, database=None):
        super().__init__(user_id, name, username, email, password, date_of_birth, role="admin")
        self.db = database  # Kết nối database

    def add_user(self, new_user):
        if not new_user.username or not new_user.email:
            raise ValueError("Username và Email không được để trống!")
        new_user.save_user()

    def reset_password(self, user_id):
        default_password = "123456789"
        try:
            self.db.cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (default_password, user_id))
            self.db.conn.commit()
            print("Mật khẩu đã được đặt lại")
        except Exception as e:
            print(f"Lỗi khi đặt lại mật khẩu: {e}")

    def delete_user(self, user_id):
        try:
            self.db.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            self.db.conn.commit()
            print("Xóa user thành công")
        except Exception as e:
            print(f"Lỗi khi xóa user: {e}")

    def add_book(self, title, author, category, published_year, quantity):
        book = Book(title, author, category, published_year, quantity)
        book.save_book()

    def edit_book(self, book_id, title=None, author=None, category=None, published_year=None, quantity=None):
        try:
            self.db.cursor.execute(
                "UPDATE books SET title = ?, author = ?, category = ?, published_year = ?, quantity = ? WHERE book_id = ?",
                (title, author, category, published_year, quantity, book_id)
            )
            self.db.conn.commit()
            print("Cập nhật sách thành công")
        except Exception as e:
            print(f"Lỗi khi cập nhật sách: {e}")

    def delete_book(self, book_id):
        try:
            self.db.cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            self.db.conn.commit()
            print("Xóa sách thành công")
        except Exception as e:
            print(f"Lỗi khi xóa sách: {e}")