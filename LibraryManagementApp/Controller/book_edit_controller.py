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
            # Set focus back to ISBN field
            self.view.entries['lnE_ISBN'].focus_set()
            return
            
        # Try to find the book
        book = Book.get_book_by_id(isbn)
        
        if not book:
            Invalid(self.view.root, 'search_book')
            # Set focus back to ISBN field
            self.view.entries['lnE_ISBN'].focus_set()
            return
        
        print(f"Book found: {book}")  # Debug print
            
        # Book found, navigate to edit screen
        self.view.root.destroy()
        
        # Create new edit screen with book data
        edit_root = Tk()
        from View.BookManagement.BookManaEditBook1 import BookEdit1App
        edit_app = BookEdit1App(edit_root, book_data=book)
        edit_root.mainloop()

    # def search_book(self):
    #     """Search for a book by ISBN and navigate to edit screen if found."""
    #     if not hasattr(self.view, 'entries') or 'lnE_ISBN' not in self.view.entries:
    #         print("Error: ISBN entry field not found")
    #         return
            
    #     isbn = self.view.entries['lnE_ISBN'].get().strip()
        
    #     # Validate ISBN format
    #     if not isbn.isdigit() or len(isbn) != 13:
    #         Invalid(self.view.root, 'Input')
    #         # Set focus back to ISBN field
    #         self.view.entries['lnE_ISBN'].focus_set()
    #         return
            
    #     # Try to find the book
    #     book = Book.get_book_by_id(isbn)
        
    #     if not book:
    #         Invalid(self.view.root, 'search_book')
    #         # Set focus back to ISBN field
    #         self.view.entries['lnE_ISBN'].focus_set()
    #         return
            
    #     # Book found, navigate to edit screen
    #     self.view.root.destroy()
        
    #     # Create new edit screen
    #     edit_root = Tk()
    #     from View.BookManagement.BookManaEditBook1 import BookEdit1App
    #     edit_app = BookEdit1App(edit_root, book_data=book)
    #     edit_root.mainloop()