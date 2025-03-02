from Database.db_lma import Database
from Model.user_model import User
from Model.book_model import Book

class Receipt:
    def __init__(self, receipt_id=None, user_id=None, book_id=None, borrow_date=None, return_date=None, status="Borrowed"):
        self.receipt_id = receipt_id
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.status = status
        self.db = Database()  

    def save(self):
        self.db.cursor.execute("INSERT INTO receipts (user_id, book_id, borrow_date, return_date, status) VALUES (?, ?, ?, ?, ?)",
                               (self.user_id, self.book_id, self.borrow_date, self.return_date, self.status))
        self.db.conn.commit()
        self.receipt_id = self.db.cursor.lastrowid

    def update_status(self, new_status):
        """Cập nhật trạng thái phiếu mượn"""
        self.db.cursor.execute("UPDATE receipts SET status = ? WHERE receipt_id = ?", 
                               (new_status, self.receipt_id))
        self.db.conn.commit()

    @staticmethod
    def get_receipt_by_id(receipt_id):
        db = Database()
        db.cursor.execute("SELECT * FROM receipts WHERE receipt_id = ?", (receipt_id,))
        return db.cursor.fetchone()
    
    @staticmethod
    def return_book(return_date, receipt_id):
        db = Database()
        db.cursor.execute("UPDATE receipts SET return_date = ?, status = 'returned' WHERE receipt_id = ?", 
                          (return_date, receipt_id))
        db.conn.commit()