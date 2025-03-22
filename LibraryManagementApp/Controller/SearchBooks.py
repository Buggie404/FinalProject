import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
import re
import datetime
import unidecode

from Model.book_model import Book
from Model.admin_model import Admin
from View.noti_tab_view_1 import Delete, Message_1, Invalid
class SearchBooks:
    """Handle book search and filtering functionality"""
    
    def __init__(self):
        pass
    
    @staticmethod
    def search_by_id(book_id):
        """Search book by exact ISBN match"""
        if not book_id:
            return False, "Please enter an ISBN to search!"
            
        # Ensure book_id is a string with 10 digits
        book_id = str(book_id).zfill(10)
        
        # Check for non-numeric characters
        if not book_id.isdigit():
            return False, "ISBN must be a series of numbers, no spaces."
        
        # Check for exactly 10 digits
        if len(book_id) != 10:
            return False, "ISBN must be exactly 10 digits long."
            
        book = Book.get_book_by_id(book_id)
        if book:
            return True, book
        return False, "No book found with this ISBN!"
    
    @staticmethod
    def search_by_title(title):
        """Search book by title (partial match)"""
        if not title or title.strip() == "":
            return False, "Please enter a title to search!"
            
        # Clean the title for search
        title = title.strip()
        title = re.sub(r'\s+', ' ', title)
            
        books = Book.search_books(title)
        if books and len(books) > 0:
            return True, books
        return False, "No books found with this title!"
    
    @staticmethod
    def search_by_category(category):
        """Search books by category"""
        if not category:
            return False, "Please select a category!"
            
        books = Book.get_book_by_category(category)
        if books and len(books) > 0:
            return True, books
        return False, f"No books found in the '{category}' category!"
    
    @staticmethod
    def filter_books(tbl_Book, search_term, load_book_func, root=None):
        """Filter books by ISBN or title"""
        # Skip filtering if search term is empty or placeholder
        if search_term == "Search" or search_term.strip() == "":
            # Reload all books
            load_book_func()
            return
            
        try:
            # Check if the search term is a number (likely an ISBN)
            is_isbn = search_term.isdigit()
            
            if is_isbn:
                print(f"Filtering by ISBN: {search_term}")
                
                # Try exact match by ISBN
                success, result = SearchBooks.search_by_id(search_term)
                
                if success:
                    # Clear existing data
                    for item in tbl_Book.get_children():
                        tbl_Book.delete(item)
                        
                    # Display the single book found
                    book = result
                    tbl_Book.insert('', 'end', values=(
                        str(book[0]),  # book_id
                        book[1],       # title
                        book[2],       # author
                        book[3],       # published_year
                        book[4],       # category
                        book[5]        # quantity
                    ))
                else:
                    # Show error message
                    Invalid(root, "Input")
                    load_book_func()
            else:
                print(f"Filtering by title: {search_term}")
                
                # Try partial match by title
                success, result = SearchBooks.search_by_title(search_term)
                
                if success:
                    # Clear existing data
                    for item in tbl_Book.get_children():
                        tbl_Book.delete(item)
                        
                    # Display all matching books
                    for book in result:
                        tbl_Book.insert('', 'end', values=(
                            str(book[0]),  # book_id
                            book[1],       # title
                            book[2],       # author
                            book[3],       # published_year
                            book[4],       # category
                            book[5]        # quantity
                        ))
                else:
                    # Show error message
                    Invalid(root, "Input")
                    load_book_func()
                    
        except Exception as e:
            print(f"Error filtering books: {e}")
            # Reload all books if filtering fails
            load_book_func()
    
    @staticmethod
    def filter_by_category(tbl_Book, category, load_book_func, root=None):
        """Filter books by category"""
        if not category:
            # Reload all books if no category selected
            load_book_func()
            return
            
        try:
            print(f"Filtering by category: {category}")
            
            # Get books by category
            success, result = SearchBooks.search_by_category(category)
            
            if success:
                # Clear existing data
                for item in tbl_Book.get_children():
                    tbl_Book.delete(item)
                    
                # Display all books in the category
                for book in result:
                    tbl_Book.insert('', 'end', values=(
                        str(book[0]),  # book_id
                        book[1],       # title
                        book[2],       # author
                        book[3],       # published_year
                        book[4],       # category
                        book[5]        # quantity
                    ))
            else:
                # Show error message
                Invalid(root, "Input")
                load_book_func()
                
        except Exception as e:
            print(f"Error filtering by category: {e}")
            # Reload all books if filtering fails
            load_book_func()
