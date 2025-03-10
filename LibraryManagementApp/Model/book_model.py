from Database.db_lma import Database

class Book:
    def __init__(self, book_id=None, title=None, author=None, category=None, published_year=None, quantity=None):
        self.book_id = book_id # Primary key
        self.title = title
        self.author = author
        self.category = category
        self.pulished_year = published_year
        self.quantity = quantity
        self.db = Database() # Connect to database
    
    def save_book(self): #To save the new added book into Database
        """
        Save a new book into the database.
        This function inserts the book title, author, published year, category, and quantity into the Books table.
        """
        self.db.cursor.execute("INSERT INTO Books (title, author, published_year, category, quantity) VALUES (?, ?, ?, ?, ?, ?)", 
                               (self.book_id, self.title, self.author, self.pulished_year, self.category, self.quantity)) 
        self.db.conn.commit()

    def update_book(self, new_data): #Update book information 
        """
        Update existing book details in the database.
        Only the title, author, category, published year, and quantity can be updated.
        """
        self.db.cursor.execute("UPDATE books SET title = ?, author = ?, category = ?, published_year = ?, quantity = ?", 
                               (new_data['title'], new_data['author'], new_data['category'], new_data['published_year'], self.book_id))
        self.db.conn.commit()
        self.book_id = self.db.cursor.lastrowid # Update book_id with the new id

    @staticmethod
    def get_book_by_id(book_id): # Search book by ID
        db = Database()
        db.cursor.execute("SELECT * FROM Books WHERE id = ?", (book_id,))
        return db.cursor.fetchone()
    
    @staticmethod
    def get_all_book(): #Display all books
        db = Database()
        db.cursor.execute("SELECT * FROM Books")
        return db.cursor.fetchall()

    @staticmethod
    def get_book_by_category(category): # Search book by category
        db = Database()
        db.cursor.execute("SELECT * FROM Books WHERE category = ?", (category,))
        return db.cursor.fetchall()

    @staticmethod
    def search_books(keyword): # Search book by title
        """
        Search for books by title. This function allows partial matching,
        meaning books with similar or related titles will also be returned.
        """
        db = Database()
        # Ensure keyword is a string 
        keyword = str(keyword) if keyword is not None else ""
        db.cursor.execute("SELECT * FROM books WHERE title LIKE ?", (f'%{keyword}%',))
        return db.cursor.fetchall()