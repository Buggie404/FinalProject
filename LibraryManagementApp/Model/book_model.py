from Database.db_lma import Database

class Book:
    def __init__(self, book_id=None, title=None, author=None, category=None, published_year=None, quantity=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.pulished_year = published_year
        self.quantity = quantity
        self.db = Database()
    
    def save_book(self):
        self.db.cursor.execute("INSERT INTO Books (title, author, published_year, category, quantity) VALUES (?, ?, ?, ?, ?)", 
                               (self.title, self.author, self.published_year, self.category, self.quantity)) 
        self.db.conn.commit()

    def update_book(self, new_data):
        """Cập nhật thông tin sách"""
        self.db.cursor.execute("UPDATE books SET title = ?, author = ?, category = ?, published_year = ?, quantity = ?", 
                               (new_data['title'], new_data['author'], new_data['category'], new_data['published_year'], self.book_id))
        self.db.conn.commit()
        self.book_id = self.db.cursor.lastrowid

    @staticmethod
    def get_book_by_id(book_id):
        db = Database()
        db.cursor.execute("SELECT * FROM Books WHERE id = ?", (book_id,))
        return db.cursor.fetchone()

    @staticmethod
    def get_book_by_title(title):
        db = Database()
        db.cursor.execute("SELECT * FROM Books WHERE title = ?", (title,))
        return db.cursor.fetchone()
    
    @staticmethod
    def get_all_book():
        db = Database()
        db.cursor.execute("SELECT * FROM Books")
        return db.cursor.fetchall()

    @staticmethod
    def search_books(keyword):
        db = Database()
        db.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR book_id = ?", 
                          (f'%{keyword}%', keyword if keyword.isdigit() else -1, f'%{keyword}%'))
        return db.cursor.fetchall()

    @staticmethod
    def get_book_by_category(category):
        db = Database()
        db.cursor.execute("SELECT * FROM Books WHERE category = ?", (category,))
        return db.cursor.fetchall()
