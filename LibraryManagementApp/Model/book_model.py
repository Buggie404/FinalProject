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
    
    def save_book(self):
        #To save the new added book into Database
        """ Save a new book into the database.
        This function inserts the book ID, title, author, published year, category, and quantity into the Books table.
        """
        self.db.cursor.execute("INSERT INTO Books (book_id, title, author, published_year, category, quantity) VALUES (?, ?, ?, ?, ?, ?)",
                            (self.book_id, self.title, self.author, self.pulished_year, self.category, self.quantity))
        self.db.conn.commit()

    def update_book(self, new_data): #Update book information 
        """Update existing book details in the database.
        Only the title, author, category, published year, and quantity can be updated.
        """
        try:
            self.db.cursor.execute(
                "UPDATE Books SET title = ?, author = ?, published_year = ?, category = ?, quantity = ? WHERE book_id = ?",
                (
                    new_data['title'],
                    new_data['author'],
                    new_data['published_year'],
                    new_data['category'],
                    new_data['quantity'],
                    self.book_id
                )
            )
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating book: {e}")
            return False

        # """
        # Update existing book details in the database.
        # Only the title, author, category, published year, and quantity can be updated.
        # """
        # self.db.cursor.execute("UPDATE books SET title = ?, author = ?, category = ?, published_year = ?, quantity = ? WHERE book_id = ?", 
        #                        (new_data['title'], new_data['author'], new_data['category'], new_data['published_year'], new_data['quantity'], self.book_id))
        # self.db.conn.commit()

    # @staticmethod
    # def get_book_by_id(book_id):
    #     # Search book by ID
    #     db = Database()
    #     # Ensure book_id is treated as string to preserve leading zeros
    #     book_id = str(book_id)
    #     db.cursor.execute("SELECT * FROM Books WHERE book_id = ? ", (book_id,))
    #     return db.cursor.fetchone()
    @staticmethod
    def get_book_by_id(book_id):
        # Search book by ID
        db = Database()
        
        # Ensure book_id is a string with 10 digits (padded with leading zeros if needed)
        book_id = str(book_id).zfill(10)
        
        db.cursor.execute("SELECT * FROM Books WHERE book_id = ? ", (book_id,))
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
        db.cursor.execute("SELECT * FROM Books WHERE title LIKE ?", (f'%{keyword}%',))
        return db.cursor.fetchall()
    
    @staticmethod
    def get_quantity(book_id):
        db = Database()
        db.cursor.execute("SELECT quantity FROM Books WHERE book_id = ?", (book_id,))
        result = db.cursor.fetchone()  # Fetch one row
        
        if result:  # Check if result is not None
            return result[0]  # Return quantity
        else:
            return None  # Handle case where book_id does not exist
