from Database.db_lma import Database
from Model.user_model import User
from Model.book_model import Book

class Receipt:
    def __init__(self, receipt_id=None, user_id=None, book_id=None, 
                 quantity=1, borrow_date=None, return_date=None, status="Borrowed"):
        self.receipt_id = receipt_id  # Primary key
        self.user_id = user_id  # Foreign key
        self.book_id = book_id  # Foreign key
        self.quantity = quantity  # Number of books borrowed
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.status = status
        self.db = Database()

    def save_receipt(self):
        # Add new receipt to database
        if not User.get_id(self.user_id) or not Book.get_book_by_id(self.book_id):
            return False  # Either user or book doesn't exist
        
        self.db.cursor.execute("INSERT INTO receipts (user_id, book_id, quantity, borrow_date, return_date, status) VALUES (?, ?, ?, ?, ?, ? )", 
                              (self.user_id, self.book_id, self.quantity, self.borrow_date, self.return_date, self.status))
        self.db.conn.commit()
        self.receipt_id = self.db.cursor.lastrowid  # Get the last inserted id
        return True

    # This method creates multiple receipts for a multi-book transaction
    def save_multi_receipt(self, cart_items):
        """Create multiple receipts for a cart of books"""
        if not User.get_id(self.user_id):
            return False  # User doesn't exist
        
        receipt_ids = []
        
        # Create a receipt for each book in the cart
        for item in cart_items:
            book_id = item['book_id']
            quantity = item['quantity']
            
            if not Book.get_book_by_id(book_id):
                continue  # Skip invalid books
            
            self.db.cursor.execute(
                "INSERT INTO receipts (user_id, book_id, quantity, borrow_date, return_date, status) VALUES (?, ?, ?, ?, ?, ?)",
                (self.user_id, book_id, quantity, self.borrow_date, self.return_date, self.status)
            )
            self.db.conn.commit()
            receipt_ids.append(self.db.cursor.lastrowid)
        
        # Store the first receipt_id for reference
        if receipt_ids:
            self.receipt_id = receipt_ids[0]
            return True
        return False

    def update_status(self, new_status):
        # Update receipt status
        if not self.get_receipt_by_id(self.receipt_id):
            return False  # Receipt not found
        
        self.db.cursor.execute("UPDATE receipts SET status = ? WHERE receipt_id = ?", (new_status, self.receipt_id))
        self.db.conn.commit()
        return True
    
    def update_related_receipts_status(self, new_status):
        """Update the status of all related receipts (same user, same borrow date)"""
        # Get the receipt to find user_id and borrow_date
        receipt_data = self.get_receipt_by_id(self.receipt_id)
        if not receipt_data:
            return False  # Receipt not found
        
        # Extract user_id and borrow_date
        user_id = receipt_data[1] 
        borrow_date = receipt_data[3]  
        
        # Update all receipts with the same user_id and borrow_date
        self.db.cursor.execute(
            "UPDATE receipts SET status = ? WHERE user_id = ? AND borrow_date = ?", 
            (new_status, user_id, borrow_date)
        )
        self.db.conn.commit()
        return True

    @staticmethod
    def get_receipt_by_id(receipt_id):
        # Get receipt by ID
        db = Database()
        db.cursor.execute("SELECT * FROM receipts WHERE receipt_id = ? ", (receipt_id,))
        return db.cursor.fetchone()

    @staticmethod
    def get_related_receipts(user_id, borrow_date):
        """Get all receipts for a user created on the same date (for multi-book borrowing)"""
        db = Database()
        db.cursor.execute(
            "SELECT * FROM receipts WHERE user_id = ? AND borrow_date = ? ORDER BY receipt_id",
            (user_id, borrow_date)
        )
        return db.cursor.fetchall()

    @staticmethod
    def return_book(return_date, receipt_id):
        db = Database()
        if not Receipt.get_receipt_by_id(receipt_id):
            return False  # Receipt not found
        db.cursor.execute("UPDATE receipts SET return_date = ?, status = 'returned' WHERE receipt_id = ? ", 
                         (return_date, receipt_id))
        db.conn.commit()
        return True

    @staticmethod
    def get_status_by_receipt_id(receipt_id):
        """Fetch the status of a receipt based on its ID."""
        db = Database()
        db.cursor.execute("SELECT status FROM receipts WHERE receipt_id = ? ", 
                         (receipt_id,))
        result = db.cursor.fetchone()
        return result[0] if result else None  # Return status if found, else None
    
    @staticmethod
    def check_overdue(receipt_id): # Check if a receipt is overdue
        db = Database()
        
        # Get the receipt
        db.cursor.execute(
            "SELECT return_date, status FROM receipts WHERE receipt_id = ?", 
            (receipt_id,)
        )
        result = db.cursor.fetchone()
        
        if not result:
            return False  # Receipt not found
        
        return_date, status = result
        
        # If already marked as overdue
        if status == "Overdue":
            return True
        
        # If already returned
        if status == "Returned":
            return False
        
        # Check if current date is after return date
        import datetime
        today = datetime.datetime.now().date()
        try:
            return_date = datetime.datetime.strptime(return_date, '%Y-%m-%d').date()
            return today > return_date
        except (ValueError, TypeError):
            return False  # Invalid date format

    @staticmethod
    def mark_as_overdue(receipt_id): # Mark a receipt as overdue
        db = Database()
        if not Receipt.get_receipt_by_id(receipt_id):
            return False  # Receipt not found
        
        db.cursor.execute(
            "UPDATE receipts SET status = 'Overdue' WHERE receipt_id = ?", 
            (receipt_id,)
        )
        db.conn.commit()
        return True

