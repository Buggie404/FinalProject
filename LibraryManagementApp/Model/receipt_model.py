from Database.db_lma import Database
from Model.user_model import User
from Model.book_model import Book

class Receipt:
    def __init__(self, receipt_id=None, user_id=None, book_id=None, borrow_date=None, return_date=None, status="Borrowed"):
        self.receipt_id = receipt_id #Primary key
        self.user_id = user_id # Foreign key
        self.book_id = book_id # Foreign key
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.status = status
        self.db = Database()  

    def save_receipt(self): # Add new receipt to database
        if not User.get_id(self.user_id) or not Book.get_book_by_id(self.book_id):
            return False # Either user or book doesn't exist
        self.db.cursor.execute("INSERT INTO receipts (user_id, book_id, borrow_date, return_date, status) VALUES (?, ?, ?, ?, ?)",
                               (self.user_id, self.book_id, self.borrow_date, self.return_date, self.status))
        self.db.conn.commit()
        self.receipt_id = self.db.cursor.lastrowid # Get the last inserted id
        return True

    def update_status(self, new_status): # Update receipt status
        if not self.get_receipt_by_id(self.receipt_id):
            return False # Receipt not found
        self.db.cursor.execute("UPDATE receipts SET status = ? WHERE receipt_id = ?", 
                               (new_status, self.receipt_id))
        self.db.conn.commit()

    @staticmethod
    def get_receipt_by_id(receipt_id): # Marked book as returned
        db = Database()
        db.cursor.execute("SELECT * FROM receipts WHERE receipt_id = ?", (receipt_id,))
        return db.cursor.fetchone()
    
    @staticmethod
    def return_book(return_date, receipt_id):
        db = Database()
        if not Receipt.get_receipt_by_id(receipt_id):
            return False  # Receipt not found
        db.cursor.execute("UPDATE receipts SET return_date = ?, status = 'returned' WHERE receipt_id = ?", 
                          (return_date, receipt_id))
        db.conn.commit()
        return True
    
    @staticmethod
    def get_status_by_receipt_id(receipt_id):
        """Fetch the status of a receipt based on its ID."""
        db = Database()
        db.cursor.execute("SELECT status FROM receipts WHERE receipt_id = ?", (receipt_id,))
        result = db.cursor.fetchone()
        return result[0] if result else None  # Return status if found, else None