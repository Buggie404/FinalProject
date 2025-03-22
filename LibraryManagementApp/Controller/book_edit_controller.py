# Controller/book_edit_controller.py

import re
import datetime
import sys
import os
from pathlib import Path
from tkinter import Tk, messagebox

# Add parent directory to path to import models
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Model.book_model import Book
from View.noti_tab_view_1 import Message_2, Invalid

class BookEditController:
    def __init__(self, view=None):
        """Initialize the BookEdit controller."""
        self.view = view
        self.book_data = None
        
        # If view is provided, bind search button
        if self.view and hasattr(self.view, 'buttons') and 'btn_Search' in self.view.buttons:
            self.view.buttons['btn_Search'].config(command=self.search_book)
            
        # If view is BookManaEditBook1 and has confirm button, bind it
        if self.view and hasattr(self.view, 'buttons') and 'btn_Confirm' in self.view.buttons:
            self.view.buttons['btn_Confirm'].config(command=self.update_book)
    
    def search_book(self):
        """Search for a book by ISBN and navigate to edit screen if found."""
        if not hasattr(self.view, 'entries') or 'lnE_ISBN' not in self.view.entries:
            print("Error: ISBN entry field not found")
            return
            
        isbn = self.view.entries['lnE_ISBN'].get().strip()
        
        # Validate ISBN format
        if not isbn.isdigit() or len(isbn) != 13:
            Invalid(self.view.root, 'Input')
            return
            
        # Try to find the book
        book = Book.get_book_by_id(isbn)
        
        if not book:
            Invalid(self.view.root, 'search_book')
            return
            
        # Book found, navigate to edit screen
        self.book_data = book
        self.view.root.destroy()
        
        # Create new edit screen
        edit_root = Tk()
        from View.BookManagement.BookManaEditBook1 import BookEdit1App
        edit_app = BookEdit1App(edit_root)
        
        # Populate fields with book data
        self.populate_edit_form(edit_app, book)
        
        # Create controller for the edit screen
        edit_controller = BookEditController(edit_app)
        
        edit_root.mainloop()
    
    def populate_edit_form(self, edit_app, book_data):
        """Populate the edit form fields with book data."""
        if not hasattr(edit_app, 'entries'):
            print("Error: Entry fields not found")
            return
            
        # Map book data to entry fields
        field_mapping = {
            'lnE_ISBN': str(book_data[0]),
            'lnE_Title': book_data[1],
            'lnE_Author': book_data[2],
            'lnE_PublishedYear': str(book_data[3]),
            'lnE_Category': book_data[4],
            'lnE_Quantity': str(book_data[5])
        }
        
        # Set values in entry fields
        for field_name, value in field_mapping.items():
            if field_name in edit_app.entries:
                entry = edit_app.entries[field_name]
                entry.delete(0, 'end')
                entry.insert(0, value)
    
    def update_book(self):
        """Validate input and update book in database."""
        if not hasattr(self.view, 'entries'):
            print("Error: Entry fields not found")
            return
            
        # Get values from entry fields
        isbn = self.view.entries['lnE_ISBN'].get().strip()
        title = self.view.entries['lnE_Title'].get().strip()
        author = self.view.entries['lnE_Author'].get().strip()
        published_year = self.view.entries['lnE_PublishedYear'].get().strip()
        category = self.view.entries['lnE_Category'].get().strip()
        quantity = self.view.entries['lnE_Quantity'].get().strip()
        
        # Validate all fields
        valid, message, book_data = self.validate_all_fields(
            isbn, title, author, published_year, category, quantity
        )
        
        if not valid:
            Invalid(self.view.root, 'Input')
            return
            
        # Update book in database
        try:
            book = Book(book_id=isbn)
            success = book.update_book(book_data)
            
            if success:
                # Show success message
                Message_2(self.view.root, 'edit_book')
            else:
                Invalid(self.view.root, 'Input')
        except Exception as e:
            print(f"Error updating book: {str(e)}")
            Invalid(self.view.root, 'Input')
    
    def validate_all_fields(self, isbn, title, author, published_year, category, quantity):
        """Validate all fields and return validation result."""
        # ISBN validation (read-only, shouldn't change)
        if not isbn or not isbn.isdigit() or len(isbn) != 13:
            return False, "ISBN must be exactly 13 digits.", {}
        
        # Title validation
        if not title or title.strip() == "":
            return False, "Title cannot be empty.", {}
        if len(title.strip()) < 2 or len(title.strip()) > 255:
            return False, "Title must be between 2 and 255 characters.", {}
        
        # Format title (remove extra spaces)
        formatted_title = re.sub(r'\s+', ' ', title.strip())
        
        # Author validation
        if not author or author.strip() == "":
            return False, "Author cannot be empty.", {}
        if len(author.strip()) < 2 or len(author.strip()) > 100:
            return False, "Author must be between 2 and 100 characters.", {}
        
        # Check for numbers in author
        if re.search(r'\d', author):
            return False, "Author name cannot contain numbers.", {}
        
        # Check for allowed characters in author
        allowed_pattern = r'^[a-zA-Z\s\-\.,&]+$'
        if not re.match(allowed_pattern, author.strip()):
            return False, "Author can only contain letters, spaces, hyphens, periods, commas, and ampersands.", {}
        
        # Check for consecutive special characters
        if re.search(r'[\-]{2,}|[\. ]{2,}|[,]{2,}|[&]{2,}', author):
            return False, "Special characters cannot appear consecutively.", {}
        
        # Format author (title case for first letter of each word)
        words = author.strip().split()
        formatted_author = ' '.join([word[0].upper() + word[1:].lower() if word else '' for word in words])
        
        # Published year validation
        if not published_year or not published_year.isdigit():
            return False, "Published Year must be a number.", {}
        
        year_int = int(published_year)
        current_year = datetime.datetime.now().year
        if year_int < 1440 or year_int > current_year:
            return False, f"Published Year must be between 1440 and {current_year}.", {}
        
        # Category validation
        valid_categories = [
            "Fiction", "Non-Fiction", "Mystery", "Science", 
            "Fantasy", "History", "Romance", "Biography", 
            "Thriller", "Technology"
        ]
        
        if not category or category not in valid_categories:
            return False, f"Category must be one of: {', '.join(valid_categories)}.", {}
        
        # Quantity validation
        if not quantity or not quantity.isdigit():
            return False, "Quantity must be a positive number.", {}
        
        quantity_int = int(quantity)
        if quantity_int <= 0:
            return False, "Quantity must be greater than zero.", {}
        
        # If all validations passed, create book data dictionary
        book_data = {
            'title': formatted_title,
            'author': formatted_author,
            'published_year': year_int,
            'category': category,
            'quantity': quantity_int
        }
        
        return True, "Book updated successfully!", book_data
