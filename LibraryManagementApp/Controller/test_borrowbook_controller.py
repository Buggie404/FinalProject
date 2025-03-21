# Import Lib
import sys
import os
import datetime
from tkinter import Tk, messagebox

# Ensure Model path is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Model.user_model import User
from Model.book_model import Book
from Model.receipt_model import Receipt

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
        # Check if user exists
        user_data = User.get_id(user_id)
        if not user_data:
            return False, None, None, "No match ID!"
            
        # Check if book exists
        book_data = Book.get_book_by_id(book_id)
        if not book_data:
            return False, None, None, "No match ISBN!"
            
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
            if requested_quantity <= 0 or requested_quantity > available_quantity:
                return False, "Invalid quantity"
                
            return True, None
        except ValueError:
            return False, "Invalid quantity format"
    
    @staticmethod
    def check_borrowing_limit(user_id, requested_quantity=1):
        """
        Check if borrowing the requested quantity would exceed the user's limit
        
        Parameters:
        user_id - The ID of the user
        requested_quantity - How many books the user wants to borrow
        
        Returns:
        (can_borrow, remaining, total_borrowed) - Tuple with borrowing status
        """
        # Import required modules
        from Model.receipt_model import Receipt
        
        # Query the database to count currently borrowed books
        db = Receipt().db
        db.cursor.execute(
            "SELECT SUM(quantity) FROM receipt_items ri "
            "JOIN receipts r ON ri.receipt_id = r.receipt_id "
            "WHERE r.user_id = ? AND r.status = 'Borrowed'", 
            (user_id,)
        )
        result = db.cursor.fetchone()
        
        # If no books borrowed yet or NULL result
        total_borrowed = result[0] if result and result[0] else 0
        
        # Calculate remaining allowed borrows
        remaining = BorrowController.MAX_TOTAL_BOOKS - total_borrowed
        
        # Check if requested quantity fits within limit
        can_borrow = requested_quantity <= remaining
        
        return can_borrow, remaining, total_borrowed

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
        self.items = [item for item in self.items if item['book_id'] != book_id]
    
    def clear(self):
        """Clear the cart"""
        self.items = []
        self.user_id = None
    
    def get_total_quantity(self):
        """Get total number of books in cart"""
        return sum(item['quantity'] for item in self.items)
    
    def is_empty(self):
        """Check if cart is empty"""
        return len(self.items) == 0
    
    def set_user(self, user_id):
        """Set the user for this cart"""
        self.user_id = user_id
