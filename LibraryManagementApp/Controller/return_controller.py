# Import Lib
import sys
import os
import datetime
from tkinter import Tk, messagebox

# Ensure Model path is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from datetime import datetime, timedelta
from Model.receipt_model import Receipt
from Model.book_model import Book

class ReturnController:
    @staticmethod
    def validate_receipt_access(receipt_id, user_id=None):
        if not receipt_id:
            return (False, "No loan code provided")
            
        # Check if receipt exists
        receipt_data = Receipt.get_receipt_by_id(receipt_id)
        if not receipt_data:
            return (False, "Loan slip not found!")
            
        # If user_id is provided, verify ownership
        if user_id is not None and receipt_data[1] != user_id:
            return (False, "This receipt doesn't belong to your account!")
            
        return (True, "Valid receipt")
    @staticmethod
    def validate_receipt_status(receipt_id):
        # Check if receipt exists
        receipt_data = Receipt.get_receipt_by_id(receipt_id)
        if not receipt_data:
            return (False, "Loan slip not found!")
        
        status = receipt_data[5].lower() if receipt_data[5] else ""
        
        # Check if already returned or overdue
        if status == "returned":
            return (False, "This book has already been returned!")
        elif status == "overdue":
            return (False, "This book is marked as overdue and  has already been returned!")
        
        return (True, "Valid for return")   

    @staticmethod
    def process_return(receipt_id, user_id=None):
        is_valid, message = ReturnController.validate_receipt_access(receipt_id, user_id)   
        if not is_valid:
            return (False, None, message)


        is_valid_status, status_message = ReturnController.validate_receipt_status(receipt_id)
        if not is_valid_status:
            return (False, None, status_message)


        # Lấy dữ liệu phiếu mượn
        receipt_data = Receipt.get_receipt_by_id(receipt_id)

        # Parse borrow date
        borrow_date = receipt_data[3]
        if isinstance(borrow_date, str):
            try:
                borrow_date = datetime.strptime(borrow_date, "%Y-%m-%d")
            except ValueError:
                try:
                    borrow_date = datetime.strptime(borrow_date, "%Y/%m/%d")
                except ValueError:
                    print(f"Could not parse date: {borrow_date}")
                    return (False, None, f"Invalid date format: {borrow_date}")

        # Tính hạn trả
        return_deadline = borrow_date + timedelta(days=20)

        # Ngày trả sách hôm nay
        current_date = datetime.now()
        formatted_return_date = current_date.strftime("%Y-%m-%d")

        # So sánh hạn trả và ngày trả
        if current_date.date() <= return_deadline.date():
            receipt_status = "Returned"
        else:
            receipt_status = "Overdue"

        # Cập nhật return_date và status vào DB
        success = Receipt.update_return_status(receipt_id, formatted_return_date, receipt_status)
        if not success:
            return (False, None, "Database update failed!")

        # Cập nhật kho sách (trả về +quantity quyển)
        
        book_id = receipt_data[2]
        borrowed_quantity = Receipt.get_borrowed_quantity(receipt_id)
        Book.update_book_quantity_after_return(book_id, borrowed_quantity)

        return (True, receipt_status, "Returned book successfully!")
    
    @staticmethod
    def update_after_payment(receipt_id):
        """Update receipt status from Overdue to Returned after payment"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        success = Receipt.update_return_status(receipt_id, current_date, "Returned")
        return success

class ReturnOverdueController:
    FINE_PER_BOOK = 10000  # 10.000 VND / sách quá hạn

    @staticmethod
    def calculate_due_and_fine(receipt_id):
        """Tính tổng sách mượn (quá hạn) và tổng tiền phạt"""
        borrowed_quantity = Receipt.get_borrowed_quantity(receipt_id)

        # Số sách quá hạn = số sách mượn
        total_due_books = borrowed_quantity

        # Tiền phạt = tổng sách quá hạn * 10.000
        total_fine = total_due_books * ReturnOverdueController.FINE_PER_BOOK

        return total_due_books, total_fine
