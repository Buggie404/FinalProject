# Import Lib
import sys
import os
from tkinter import Tk, messagebox

# Ensure Model path is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from datetime import datetime, timedelta
from Model.receipt_model import Receipt
from Model.book_model import Book
from Model.user_model import User

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
            return (False, "This book is marked as overdue!")
        
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

        # Cập nhật kho sách (trả về + quantity quyển)     
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

class BorrowController:
    # Maximum books a user can borrow in total
    MAX_TOTAL_BOOKS = 5

    @staticmethod
    def validate_user_and_book(user_id, book_id):
        """
        Validate if user_id and book_id exist in the database

        Parameters:
        user_id - The ID of the user
        book_id - The ISBN of the book

        Returns:
        (is_valid, user_data, book_data, error_message) - Tuple with validation results
        """
        # Check if user_id is empty
        if not user_id:
            return False, None, None, "ID cannot be empty!"

        # Check if book_id is empty
        if not book_id:
            return False, None, None, "ISBN cannot be empty!"

        # Check if user exists
        user_data = User.get_id(user_id)
        if not user_data:
            return False, None, None, "No match ID!"

        # Check if book exists
        book_data = Book.get_book_by_id(book_id)
        if not book_data:
            return False, None, None, "No match ISBN!"
        
        # Get adjuted available quantity
        adjusted_quantity = BorrowController.get_adjusted_available_quantity(book_id)

        # Check if book is available (quantity > 0)
        available_quantity = book_data[5]  
        if available_quantity <= 0:
            return False, None, None, "Book not available for borrowing"

        return True, user_data, book_data, None

    @staticmethod
    def validate_quantity(requested_quantity, available_quantity):
        """
        Validate if the requested quantity is valid

        Parameters:
        requested_quantity - The quantity requested by the user
        available_quantity - The available quantity of the book

        Returns:
        (is_valid, error_message) - Tuple with validation result
        """
        try:
            requested_quantity = int(requested_quantity)
            
            # Check if quantity is valid (greater than 0 and less than or equal to available)
            if requested_quantity <= 0:
                return False, "Quantity must be greater than zero"

            if requested_quantity > available_quantity:
                return False, f"Only {available_quantity} copies available"

            return True, None
        except ValueError:
            return False, "Invalid quantity format"

    @staticmethod
    def check_borrowing_limit(user_id, requested_quantity=1):
        """
        Check if borrowing the requested quantity would exceed the session limit of 5 books
        
        Parameters:
        user_id - The ID of the user
        requested_quantity - How many books the user wants to borrow
        
        Returns:
        (can_borrow, remaining, cart_total)
        Tuple with borrowing status
        """
        # Get the cart instance
        cart = BorrowingCart.get_instance()

        # Count books in current cart
        cart_total = cart.get_total_quantity()

        # Calculate remaining allowed borrows
        remaining = BorrowController.MAX_TOTAL_BOOKS - cart_total

        # Check if requested quantity fits within limit
        can_borrow = requested_quantity <= remaining

        return can_borrow, remaining, cart_total

    @staticmethod
    def complete_borrowing(user_id, cart_items):
        """
        Complete the borrowing process by creating receipts and updating book quantities

        Parameters:
        user_id - The ID of the user
        cart_items - List of items in the cart

        Returns:
        (success, receipt_id, borrow_date, return_deadline) - Tuple with status and receipt info
        """
        if not cart_items:
            return False, None, None, None

        # Calculate borrow date (today) and return deadline (20 days from today)
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        return_deadline_str = (today + timedelta(days=20)).strftime('%Y-%m-%d')

        # Create receipt object
        receipt = Receipt(
            user_id=user_id,
            borrow_date=today_str,
            status="Borrowed"
        )

        # Save multiple receipts (one for each book) with the same user_id and borrow_date
        try:
            success = receipt.save_multi_receipt(cart_items)

            if not success:
                return False, None, None, None

            # Update book quantities
            for item in cart_items:
                try:
                    book_id = item['book_id']
                    quantity = item['quantity']

                    # Get current book data
                    book_data = Book.get_book_by_id(book_id)
                    if not book_data:
                        continue

                    current_quantity = book_data[5]  
                    new_quantity = current_quantity - quantity

                    # Update book quantity
                    book = Book(book_id=book_id)
                    update_result = book.update_book({
                        'title': book_data[1],
                        'author': book_data[2],
                        'category': book_data[4],
                        'published_year': book_data[3],
                        'quantity': new_quantity
                    })
                    if not update_result:
                        print(f"Warning: Failed to update quantity for book {book_id}")
                except Exception as e:
                    print(f"Error updating book {book_id}: {e}")
                    import traceback
                    traceback.print_exc()
                    
            # Return success status, receipt ID, borrow date, and return deadline
            return True, receipt.receipt_id, today_str, return_deadline_str
            
        except Exception as e:
            print(f"Error in complete_borrowing: {e}")
            import traceback
            traceback.print_exc()
            return False, None, None, None

            #         if not update_result:
            #             pass
            #     except Exception as e:
            #         print(f"Error updating book {book_id}: {e}")
            #         import traceback
            #         traceback.print_exc()

            # # Return success status, receipt ID, borrow date, and return deadline
            # return True, receipt.receipt_id, today_str, return_deadline_str

        except Exception as e:
            print(f"Error in complete_borrowing: {e}")
            import traceback
            traceback.print_exc()
            return False, None, None, None
        
    @staticmethod
    def get_adjusted_available_quantity(book_id):
        """
        Get the available quantity of a book, adjusted for what's already in the cart
        
        Parameters:
        book_id - The ID of the book
        
        Returns:
        adjusted_quantity - The available quantity minus what's in the cart
        """

        # Get database quantity
        db_quantity = Book.get_book_by_id(book_id)[5]

        if db_quantity is None:
            return 0
        
        # Get the cart instance
        cart = BorrowingCart.get_instance()

        # Find if this book is in the cart
        cart_quantity = 0
        for item in cart.items:
            if item['book_id']== book_id:
                cart_quantity = item['quantity']

        # Calculate adjusted quantitiy
        adjusted_quantity = db_quantity - cart_quantity

        return max(0, adjusted_quantity)

class BorrowingCart:
    _instance = None

    @classmethod
    def get_instance(cls):
        """Singleton pattern to ensure we have one cart across the application"""
        if cls._instance is None:
            cls._instance = BorrowingCart()
        return cls._instance

    def __init__(self):
        self.items = []  # List of items in cart
        self.user_id = None  # User who owns this cart

    def add_item(self, book_id, title, quantity):
        """Add a book to the cart"""
        # Ensure quantity is an integer
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            quantity = 1

        # If this is the first item, store the user_id
        if not self.user_id and hasattr(self, 'user_id'):
            self.user_id = self.user_id

        # Check if book already in cart
        for item in self.items:
            if item['book_id'] == book_id:
                # Update quantity instead of adding new item
                item['quantity'] += quantity
                return True

        # Add new item
        self.items.append({
            'book_id': book_id,
            'title': title,
            'quantity': quantity
        })
        return True

    def remove_item(self, book_id):
        """Remove a book from the cart"""
        original_len = len(self.items)
        self.items = [item for item in self.items if item['book_id'] != book_id]
        if len(self.items) < original_len:
            print(f"Removed book_id={book_id} from cart")
        else:
            print(f"Book_id={book_id} not found in cart")

    def clear(self):
        """Clear the cart"""
        self.items = []
        self.user_id = None

    def get_total_quantity(self):
        """Get total number of books in cart"""
        total = sum(item['quantity'] for item in self.items)
        return total

    def is_empty(self):
        """Check if cart is empty"""
        is_empty = len(self.items) == 0
        return is_empty

    def set_user(self, user_id):
        """Set the user for this cart"""
        self.user_id = user_id