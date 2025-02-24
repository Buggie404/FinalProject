class Receipt:
    def __init__(self, receipt_id=None, user_id=None, book_id=None, borrow_date=None, return_date=None, status="Borrowed"):
        self.receipt_id = receipt_id
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.status = status
        # self.db = Database()  # Kết nối database khi cần
    def save(self):
        pass
    def get_receipt_by_id(self, receipt_id):
        pass
    def return_book(self):
        pass