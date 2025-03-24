from Database.db_lma import Database
from Model.user_model import User
from Model.book_model import Book

class Receipt:
    def __init__(self, receipt_id=None, user_id=None, book_id=None, quantity=1, borrow_date=None, return_date=None, status="Borrowed"):
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

        self.db.cursor.execute("INSERT INTO receipts (user_id, book_id, borrowed_quantity, borrow_date, return_date, status) VALUES (?, ?, ?, ?, ?, ? )",
                              (self.user_id, self.book_id, self.quantity, self.borrow_date, self.return_date, self.status))
        self.db.conn.commit()
        self.receipt_id = self.db.cursor.lastrowid  # Get the last inserted id
        return True

    # This method creates multiple receipts for a multi-book transaction
    def save_multi_receipt(self, cart_items):
        """Create a receipt for a cart of books"""
        if not User.get_id(self.user_id):
            print(f"User ID {self.user_id} not found")
            return False  # User doesn't exist

        try:
            print(f"Starting save_multi_receipt with {len(cart_items)} items")
            
            # If there's only one book in the cart, process it normally
            if len(cart_items) == 1:
                book_id = cart_items[0]['book_id']
                quantity = cart_items[0]['quantity']
                
                self.db.cursor.execute(
                    "INSERT INTO receipts (user_id, book_id, borrowed_quantity, borrow_date, return_date, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (self.user_id, book_id, quantity, self.borrow_date, self.return_date, self.status)
                )
                self.db.conn.commit()
                self.receipt_id = self.db.cursor.lastrowid
                print(f"Created single receipt with ID: {self.receipt_id} for book {book_id}")
                return True
            
            # For multiple books, create separate receipts for each book
            # but track the first receipt_id to return to the caller
            first_receipt_id = None
            
            for i, item in enumerate(cart_items):
                book_id = item['book_id']
                quantity = item['quantity']
                
                if not Book.get_book_by_id(book_id):
                    print(f"Invalid book ID: {book_id}, skipping")
                    continue  # Skip invalid books
                
                try:
                    # Create a separate receipt for each book
                    self.db.cursor.execute(
                        "INSERT INTO receipts (user_id, book_id, borrowed_quantity, borrow_date, return_date, status) VALUES (?, ?, ?, ?, ?, ?)",
                        (self.user_id, book_id, quantity, self.borrow_date, self.return_date, self.status)
                    )
                    self.db.conn.commit()
                    
                    # Store the first receipt_id to return
                    receipt_id = self.db.cursor.lastrowid
                    if i == 0:
                        first_receipt_id = receipt_id
                        self.receipt_id = first_receipt_id
                    
                    # Store the first receipt_id to return
                    if i == 0:
                        self.receipt_id = receipt_id
                    
                    print(f"Created receipt {receipt_id} for book {book_id}, quantity {quantity}")
                except Exception as e:
                    self.db.conn.rollback()
                    print(f"Error creating receipt for book {book_id}: {e}")
                    import traceback
                    traceback.print_exc()
            
            # If at least one receipt was created successfully
            if self.receipt_id:
                return True
            else:
                print("No receipts were created successfully")
                return False
                
        except Exception as e:
            self.db.conn.rollback()
            print(f"Error in save_multi_receipt: {e}")
            import traceback
            traceback.print_exc()
            return False

    def update_status(self, new_status):
        # Update receipt status
        if not self.get_receipt_by_id(self.receipt_id):
            return False  # Receipt not found

        self.db.cursor.execute("UPDATE receipts SET status = ? WHERE receipt_id = ? ", (new_status, self.receipt_id))
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
            "UPDATE receipts SET status = ? WHERE user_id = ? AND borrow_date = ? ",
            (new_status, user_id, borrow_date)
        )
        self.db.conn.commit()
        return True

    @staticmethod
    def get_single_receipt_by_id(receipt_id):
        # Get receipt by ID
        db = Database()
        db.cursor.execute("""
            SELECT receipt_id, user_id, book_id, borrow_date, return_date, status, borrowed_quantity
            FROM receipts
            WHERE receipt_id = ?
        """, (receipt_id,))
        return db.cursor.fetchone()

    @staticmethod
    def get_related_receipts(user_id, borrow_date):
        """Get all receipts with the same user_id and borrow_date"""
        db = Database()
        db.cursor.execute("""
            SELECT receipt_id, user_id, book_id, borrow_date, return_date, status, borrowed_quantity
            FROM receipts
            WHERE user_id = ? AND borrow_date = ?
            ORDER BY book_id
        """, (user_id, borrow_date))
        return db.cursor.fetchall()

    @staticmethod
    def return_book(return_date, receipt_id):
        db = Database()
        
        # Get the receipt to find user_id and borrow_date
        receipt_data = Receipt.get_receipt_by_id(receipt_id)
        if not receipt_data:
            return False  # Receipt not found
            
        # Update this specific receipt
        db.cursor.execute("""
            UPDATE receipts 
            SET return_date = ?, status = 'returned' 
            WHERE receipt_id = ?
        """, (return_date, receipt_id))
        
        db.conn.commit()
        return True

    @staticmethod
    def return_related_books(return_date, user_id, borrow_date):
        """Return all books borrowed by a user on the same date"""
        db = Database()
        
        # Update all receipts with the same user_id and borrow_date
        db.cursor.execute("""
            UPDATE receipts 
            SET return_date = ?, status = 'returned' 
            WHERE user_id = ? AND borrow_date = ?
        """, (return_date, user_id, borrow_date))
        
        db.conn.commit()
        return True

    @staticmethod
    def get_receipt_by_id(receipt_id):
        # Get receipt by ID
        db = Database()
        
        db.cursor.execute("""
            SELECT r.receipt_id, r.user_id, r.book_id, r.borrow_date, r.return_date, r.status, r.borrowed_quantity
            FROM receipts r
            WHERE r.receipt_id = ?
        """, (receipt_id,))

        return db.cursor.fetchone()

    @staticmethod
    def check_overdue(receipt_id):
        # Check if a receipt is overdue
        db = Database()

        # Get the receipt
        db.cursor.execute(
            "SELECT return_date, status FROM receipts WHERE receipt_id = ? ",
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
    def mark_as_overdue(receipt_id):
        # Mark a receipt as overdue
        db = Database()
        if not Receipt.get_receipt_by_id(receipt_id):
            return False  # Receipt not found

        db.cursor.execute(
            "UPDATE receipts SET status = 'Overdue' WHERE receipt_id = ? ",
            (receipt_id,)
        )
        db.conn.commit()
        return True

    @staticmethod
    def check_table_schema():
        """Check the schema of the receipts table and print column names"""
        db = Database()
        db.cursor.execute("PRAGMA table_info(receipts)")
        columns = db.cursor.fetchall()
        print("Receipts table schema:")
        for column in columns:
            print(f"Column: {column[1]}, Type: {column[2]}")

    @staticmethod
    def update_return_status(receipt_id, return_date, status):
        db = Database()
        try:
            db.cursor.execute("""
                UPDATE receipts 
                SET return_date = ?, status = ? 
                WHERE receipt_id = ?
            """, (return_date, status, receipt_id))
            
            db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating receipt status: {e}")
            return False

    @staticmethod
    def get_borrowed_quantity(receipt_id):
        db = Database()
        query = "SELECT borrowed_quantity FROM receipts WHERE receipt_id = ?"
        result = db.cursor.execute(query, (receipt_id,)).fetchone()
        return result[0] if result else 0
        
    def is_already_returned(receipt_id):
        db = Database()
        
        # Get the receipt status
        db.cursor.execute(
            "SELECT status FROM receipts WHERE receipt_id = ? ",
            (receipt_id,)
        )
        result = db.cursor.fetchone()
        
        if not result:
            return False, "Receipt not found"  # Receipt not found
        
        status = result[0].lower() if result[0] else ""
        
        # Return True if already returned or overdue
        if status == "Returned":
            return True, "This book has already been returned!"
        elif status == "Overdue":
            return True, "This book is marked as overdue and has already been returned!"
        
        return False, "Book is available for return"