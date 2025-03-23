# import re
# import datetime
# import sys
# import os
# from pathlib import Path
# from tkinter import Tk, messagebox

# # Add parent directory to path to import models
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

# from Model.book_model import Book
# from View.noti_tab_view_1 import Message_2, Invalid

# class BookEditController:
#     def __init__(self, view=None):
#         """Initialize the BookEdit controller."""
#         self.view = view
#         self.book_data = None
        
#         # If view is provided, bind search button
#         if self.view and hasattr(self.view, 'buttons') and 'btn_Search' in self.view.buttons:
#             self.view.buttons['btn_Search'].config(command=self.search_book)
            
#         # If view is BookManaEditBook1 and has confirm button, bind it
#         if self.view and hasattr(self.view, 'buttons') and 'btn_Confirm' in self.view.buttons:
#             self.view.buttons['btn_Confirm'].config(command=self.update_book)

#     def search_book(self):
#         """Search for a book by ISBN and navigate to edit screen if found."""
#         if not hasattr(self.view, 'entries') or 'lnE_ISBN' not in self.view.entries:
#             print("Error: ISBN entry field not found")
#             return
            
#         isbn = self.view.entries['lnE_ISBN'].get().strip()
        
#         # Validate ISBN format
#         if not isbn.isdigit() or len(isbn) != 13:
#             messagebox.showerror("Invalid ISBN", "ISBN must be exactly 13 digits.")
#             # Set focus back to ISBN field
#             self.view.entries['lnE_ISBN'].focus_set()
#             return
            
#         # Try to find the book
#         book = Book.get_book_by_id(isbn)
        
#         if not book:
#             messagebox.showerror("Book Not Found", "No book found with this ISBN in the database.")
#             # Set focus back to ISBN field
#             self.view.entries['lnE_ISBN'].focus_set()
#             return
            
#         print(f"Book found: {book}")  # Debug print
        
#         # Book found, navigate to edit screen
#         self.view.root.destroy()
        
#         # Create new edit screen with book data
#         edit_root = Tk()
#         from View.BookManagement.BookManaEditBook1 import BookEdit1App
#         edit_app = BookEdit1App(edit_root, book_data=book)
#         edit_root.mainloop()
        
#     def update_book(self):
#         """Update book information in database."""
#         # This method is called from the view's update_book method
#         # The view already handles validation and data collection
#         pass
        
#     def update_book_data(self, book_id, updated_data):
#         """Update book data in the database."""
#         try:
#             # Create a Book object with the original book_id
#             book = Book(book_id=book_id)
            
#             # Update the book with new data
#             success = book.update_book(updated_data)
            
#             return success
#         except Exception as e:
#             print(f"Error updating book: {e}")
#             return False
            
#     def validate_title(self, title):
#         """Validate book title."""
#         if not title or title.strip() == "":
#             return False, "Title cannot be empty."
            
#         # Check length
#         if len(title.strip()) < 2:
#             return False, "Title must be at least 2 characters."
#         if len(title.strip()) > 255:
#             return False, "Title must be at most 255 characters."
            
#         return True, ""
        
#     def validate_author(self, author):
#         """Validate book author."""
#         if not author or author.strip() == "":
#             return False, "Author cannot be empty."
            
#         # Check length
#         if len(author.strip()) < 2:
#             return False, "Author must be at least 2 characters."
#         if len(author.strip()) > 100:
#             return False, "Author must be at most 100 characters."
            
#         # Check for numbers
#         if re.search(r'\d', author):
#             return False, "Author name cannot contain numbers."
            
#         # Check for allowed characters
#         if not re.match(r'^[a-zA-ZÀ-ỹ\s\-\.,&]+$', author):
#             return False, "Only letters, spaces, hyphens (-), periods (.), commas (,), and ampersands (&) are allowed."
            
#         # Check for consecutive special characters
#         if re.search(r'[\-]{2,}|[\. ]{2,}|[,]{2,}|[&]{2,}', author):
#             return False, "Special characters (., -, comma, &) cannot appear consecutively."
            
#         return True, ""
        
#     def validate_published_year(self, year):
#         """Validate published year."""
#         if not year or year.strip() == "":
#             return False, "Published Year cannot be empty."
            
#         # Check if it's a number
#         if not year.isdigit():
#             return False, "Published Year must be a number."
            
#         # Check range
#         year_int = int(year)
#         current_year = datetime.datetime.now().year
        
#         if year_int < 1440 or year_int > current_year:
#             return False, f"Published Year must be between 1440 and {current_year}."
            
#         return True, ""
        
#     def validate_category(self, category):
#         """Validate book category."""
#         if not category or category.strip() == "":
#             return False, "Category cannot be empty."
            
#         # Valid categories list
#         valid_categories = [
#             "Fiction", "Non-Fiction", "Mystery", "Science", 
#             "Fantasy", "History", "Romance", "Biography", 
#             "Thriller", "Technology"
#         ]
        
#         # Check if category is valid
#         if category not in valid_categories:
#             return False, f"Category must be one of: {', '.join(valid_categories)}."
            
#         return True, ""
        
#     def validate_quantity(self, quantity):
#         """Validate book quantity."""
#         if not quantity or quantity.strip() == "":
#             return False, "Quantity cannot be empty."
            
#         # Check if it's a number
#         if not quantity.isdigit():
#             return False, "Quantity must be a positive integer."
            
#         # Check if it's positive
#         quantity_int = int(quantity)
#         if quantity_int <= 0:
#             return False, "Quantity must be greater than zero."
            
#         return True, ""