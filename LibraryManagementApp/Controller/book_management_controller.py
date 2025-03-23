import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
import re
import datetime
import unidecode
from pathlib import Path
from tkinter import Tk, messagebox

from Model.book_model import Book
from Model.admin_model import Admin
from View.noti_tab_view_1 import Delete, Message_1, Invalid, Message_2

# from View.BookManaAddBook import BookManagementAddBookApp
# from View.BookManaAddBook1 import BookManaAddBook1App

class SearchBooks:
    """Handle book search and filtering functionality"""
   
    def __init__(self):
        pass
   
    @staticmethod
    def search_by_id(book_id):
        """Search book by exact ISBN match"""
        if not book_id:
            return False, "Please enter an ISBN to search!"
           
        # Ensure book_id is a string with 13 digits
        book_id = str(book_id).zfill(13)
       
        # Check for non-numeric characters
        if not book_id.isdigit():
            return False, "ISBN must be a series of numbers, no spaces."
       
        # Check for exactly 13 digits
        if len(book_id) != 13:
            return False, "ISBN must be exactly 13 digits long."
           
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
                    Message_1(root, "search_book")
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
                    Message_1(root, "search_book")
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
                Message_1(root, "search_book")
                load_book_func()
               
        except Exception as e:
            print(f"Error filtering by category: {e}")
            # Reload all books if filtering fails
            load_book_func()

class DeleteBook:
    def __init__(self, view):
        """Initialize the DeleteBook controller."""
        self.view = view
        self.admin = None
        self.selected_book_id = None
        
        # Bind delete button event
        self.view.buttons["btn_DeleteBook"].config(command=self.delete_selected_book)
        
        # Bind book selection event
        self.view.tbl_Book.bind("<<TreeviewSelect>>", self.on_book_select)
    
    def set_admin(self, admin):
        """Set the admin user for performing admin operations."""
        self.admin = admin
    
    def on_book_select(self, event):
        """Handle book selection in the table."""
        selected_items = self.view.tbl_Book.selection()
        if selected_items:
            item = self.view.tbl_Book.item(selected_items[0])
            self.selected_book_id = str(item["values"][0]).zfill(10)
            print(f"Selected book ID: {self.selected_book_id}")
        else:
            self.selected_book_id = None
    
    def delete_selected_book(self):
        """Show delete confirmation dialog and handle deletion."""
        if not self.selected_book_id:
            print("❌ No book selected.")
            return
        
        print(f"🗑️ Attempting to delete book ID: {self.selected_book_id}")
        delete_dialog = Delete(self.view.root, "book")
        delete_dialog.set_yes_callback(self.confirm_delete_book)
    
    def confirm_delete_book(self):
        """Delete the selected book from database and UI."""
        if not self.admin:
            print("❌ Admin not set")
            return
        
        book_id_to_delete = self.selected_book_id.zfill(10)
        selected_items = self.view.tbl_Book.selection()
        selected_item = selected_items[0] if selected_items else None
        
        if not selected_item:
            print("❌ No item selected in the table")
            return
        
        success = self.admin.delete_book(book_id_to_delete)
        
        if success:
            print(f"✅ Successfully deleted book ID: {book_id_to_delete}")
            self.view.tbl_Book.delete(selected_item)
            Message_1(self.view.root, "book")
            self.selected_book_id = None
        else:
            print("❌ Failed to delete book from database")
            Invalid(self.view.root, "input")

class add_book:
    """Controller handles admin book addition operations"""
   
    # Valid categories list
    valid_categories = [
        "Fiction", "Non-Fiction", "Mystery", "Science",
        "Fantasy", "History", "Romance", "Biography",
        "Thriller", "Technology"
    ]
   
    # Field validation errors tracking
    field_validation_errors = {
        'isbn': False,
        'title': False,
        'author': False,
        'published_year': False,
        'category': False,
        'quantity': False
    }
   
    @staticmethod
    def process_book_form(isbn, title, author, published_year, category, quantity):
        """
        Process book form data, validate it, and create a new book
       
        Args:
            isbn (str): Book ISBN code
            title (str): Book title
            author (str): Book author
            published_year (str): Year of publication
            category (str): Book category
            quantity (str): Book quantity
           
        Returns:
            tuple: (success_flag, message, book_data)
        """
        # Reset validation errors for a fresh form submission
        field_errors = {
            'isbn': False,
            'title': False,
            'author': False,
            'published_year': False,
            'category': False,
            'quantity': False
        }
       
        # Check for empty fields first
        if not isbn or isbn.strip() == "":
            return False, "ISBN cannot be empty", {}
        if not title or title.strip() == "":
            return False, "Title cannot be empty", {}
        if not author or author.strip() == "":
            return False, "Author cannot be empty", {}
        if not published_year or published_year.strip() == "":
            return False, "Published Year cannot be empty", {}
        if not category or category.strip() == "":
            return False, "Category cannot be empty", {}
        if not quantity or quantity.strip() == "":
            return False, "Quantity cannot be empty", {}
       
        # Validate all fields at once and collect errors
        valid_isbn, isbn_msg = add_book.validate_isbn(isbn)
        if not valid_isbn:
            field_errors['isbn'] = True
            return False, isbn_msg, {}
       
        valid_title, title_msg, formatted_title = add_book.validate_title(title)
        if not valid_title:
            field_errors['title'] = True
            return False, title_msg, {}
       
        valid_author, author_msg, formatted_author = add_book.validate_author(author)
        if not valid_author:
            field_errors['author'] = True
            return False, author_msg, {}
       
        valid_year, year_msg, formatted_year = add_book.validate_published_year(published_year)
        if not valid_year:
            field_errors['published_year'] = True
            return False, year_msg, {}
       
        valid_category, category_msg = add_book.validate_category(category)
        if not valid_category:
            field_errors['category'] = True
            return False, category_msg, {}
       
        valid_quantity, quantity_msg, formatted_quantity = add_book.validate_quantity(quantity)
        if not valid_quantity:
            field_errors['quantity'] = True
            return False, quantity_msg, {}
       
        # If we got here, all validations passed
        # Create book data dictionary
        book_data = {
            'book_id': isbn,  # Using ISBN as book_id
            'title': formatted_title,
            'author': formatted_author,
            'published_year': formatted_year,
            'category': category,
            'quantity': formatted_quantity
        }
       
        # Create and save book
        try:
            admin = Admin()  # Create admin instance to add book
            success = admin.add_book(
                book_id=isbn,
                title=formatted_title,
                author=formatted_author,
                category=category,
                published_year=formatted_year,
                quantity=formatted_quantity
            )
           
            if not success:
                return False, "Failed to save book to database. The book might already exist.", {}
               
            # Reset validation errors after successful save
            add_book.field_validation_errors = {k: False for k in field_errors}
           
            return True, "Book added successfully!", book_data
           
        except Exception as e:
            return False, f"Error creating book: {str(e)}", {}
   
    @staticmethod
    def validate_isbn_on_event(isbn):
        """
        Validate ISBN field when focus leaves the field
       
        Args:
            isbn (str): ISBN to validate
           
        Returns:
            tuple: (is_valid, error_message)
        """
        valid, message = add_book.validate_isbn(isbn)
        add_book.field_validation_errors['isbn'] = not valid
        return valid, message
   
    @staticmethod
    def validate_isbn(isbn):
        """
        Validate that ISBN contains only positive integers, no spaces
       
        Args:
            isbn (str): ISBN to validate
           
        Returns:
            tuple: (is_valid, error_message)
        """
        if not isbn or isbn.strip() == "":
            return False, "ISBN cannot be empty."
       
        # Remove spaces
        isbn = isbn.strip()
       
        # Check for non-numeric characters
        if not isbn.isdigit():
            return False, "ISBN must be a series of numbers, no spaces."
        #Check for exactly 13 digits
        if len(isbn) != 13:
            return False, "ISBN must be exactly 13 digits long."
       
        # Check if ISBN already exists
        if Book.get_book_by_id(isbn):
            return False, "ISBN already exists in the system. Please check the ISBN."
       
        return True, ""
   
    @staticmethod
    def validate_title_on_event(title):
        """
        Validate title field when focus leaves the field
       
        Args:
            title (str): Title to validate
           
        Returns:
            tuple: (is_valid, error_message)
        """
        valid, message, _ = add_book.validate_title(title)
        add_book.field_validation_errors['title'] = not valid
        return valid, message
   
    @staticmethod
    def validate_title(title):
        """
        Validate book title with support for Vietnamese characters
       
        Args:
            title (str): Title to validate
           
        Returns:
            tuple: (is_valid, error_message, formatted_title)
        """
        if not title or title.strip() == "":
            return False, "Title cannot be empty.", ""
       
        # Check length
        if len(title.strip()) < 2:
            return False, "Length: 2 to 255 characters.", ""
        if len(title.strip()) > 255:
            return False, "Length: 2 to 255 characters.", ""
       
        # Remove extra spaces at beginning and end
        formatted_title = title.strip()
       
        # Standardize multiple spaces to single space
        formatted_title = re.sub(r'\s+', ' ', formatted_title)
       
        # Convert to ASCII for validation but keep original for storage
        ascii_title = unidecode.unidecode(formatted_title)
       
        return True, "", formatted_title
   
    @staticmethod
    def validate_author_on_event(author):
        """
        Validate author field when focus leaves the field
       
        Args:
            author (str): Author to validate
           
        Returns:
            tuple: (is_valid, error_message)
        """
        valid, message, _ = add_book.validate_author(author)
        add_book.field_validation_errors['author'] = not valid
        return valid, message

    @staticmethod
    def validate_author(author):
        """
        Validate book author with support for Vietnamese characters, multiple authors,
        and special formatting rules
       
        Args:
            author (str): Author to validate
           
        Returns:
            tuple: (is_valid, error_message, formatted_author)
        """
        if not author or author.strip() == "":
            return False, "Author cannot be empty.", ""
       
        # Check length
        if len(author.strip()) < 2:
            return False, "Length: 2 to 100 characters.", ""
        if len(author.strip()) > 100:
            return False, "Length: 2 to 100 characters.", ""
       
        # Remove extra spaces at beginning and end
        author = author.strip()
       
        # Convert to ASCII for validation but keep original for storage
        ascii_author = unidecode.unidecode(author)
       
        # Check for numbers
        if re.search(r'\d', ascii_author):
            return False, "Special characters (@, #, $, %, *, etc.) and numbers are not allowed.", ""
       
        # Check for allowed characters (after conversion to ASCII)
        # Now including commas and ampersands for multiple authors
        allowed_pattern = r'^[a-zA-Z\s\-\.,&]+$'
        if not re.match(allowed_pattern, ascii_author):
            return False, "Only letters, spaces, hyphens (-), periods (.), commas (,), and ampersands (&) are allowed.", ""
       
        # Check for consecutive special characters (2 or more) - EXCLUDING SPACES
        if re.search(r'[\-]{2,}|[\.]{2,}|[,]{2,}|[&]{2,}', author):
            return False, "Special characters (., -, comma, &) cannot appear consecutively.", ""
       
        # Improved title case function that preserves case after periods and hyphens
        def smart_title_case(text):
            # Split by spaces
            words = text.split()
            result = []
           
            for word in words:
                # If word contains special characters like period or hyphen
                if '.' in word or '-' in word or ',' in word or '&' in word:
                    # Split by special characters and keep them
                    parts = []
                    current = ""
                    for char in word:
                        if char in '.-,&':
                            if current:
                                parts.append(current)
                                current = ""
                            parts.append(char)
                        else:
                            current += char
                    if current:
                        parts.append(current)
                   
                    # Process each part
                    processed_parts = []
                    for i, part in enumerate(parts):
                        if part in '.-,&':
                            processed_parts.append(part)
                        elif i == 0 or parts[i-1] in '.-':
                            # Capitalize if it's the first part or follows a period or hyphen
                            processed_parts.append(part[0].upper() + part[1:].lower() if part else "")
                        else:
                            # Otherwise lowercase
                            processed_parts.append(part.lower())
                   
                    result.append(''.join(processed_parts))
                else:
                    # Regular word - capitalize first letter
                    result.append(word[0].upper() + word[1:].lower() if word else "")
           
            return ' '.join(result)
       
        # Apply smart title case
        formatted_author = smart_title_case(author)
       
        # Standardize multiple spaces to single space in the final result
        formatted_author = re.sub(r'\s+', ' ', formatted_author)
       
        return True, "", formatted_author


    @staticmethod
    def validate_published_year_on_event(year):
        """
        Validate published year field when focus leaves the field
       
        Args:
            year (str): Year to validate
           
        Returns:
            tuple: (is_valid, error_message)
        """
        valid, message, _ = add_book.validate_published_year(year)
        add_book.field_validation_errors['published_year'] = not valid
        return valid, message
   
    @staticmethod
    def validate_published_year(year):
        """
        Validate published year
       
        Args:
            year (str): Year to validate
           
        Returns:
            tuple: (is_valid, error_message, formatted_year)
        """
        if not year or year.strip() == "":
            return False, "Published Year cannot be empty.", ""
       
        # Remove spaces
        year = year.strip()
       
        # Check if it's a positive integer
        if not year.isdigit():
            return False, "Please enter the number of years between 1440 and the current year.", ""
       
        # Convert to integer
        year_int = int(year)
        current_year = datetime.datetime.now().year
       
        # Check range
        if year_int < 1440 or year_int > current_year:
            return False, f"Please enter the number of years between 1440 and {current_year}.", ""
       
        return True, "", year_int
   
    @staticmethod
    def validate_category_on_event(category):
        """
        Validate category field when focus leaves the field
       
        Args:
            category (str): Category to validate
           
        Returns:
            tuple: (is_valid, error_message)
        """
        valid, message = add_book.validate_category(category)
        add_book.field_validation_errors['category'] = not valid
        return valid, message
   
    @staticmethod
    def validate_category(category):
        """
        Validate book category
       
        Args:
            category (str): Category to validate
           
        Returns:
            tuple: (is_valid, error_message)
        """
        if not category or category.strip() == "":
            return False, "Category cannot be empty."
       
        # Check if category is in the valid list
        if category not in add_book.valid_categories:
            categories_str = ", ".join(add_book.valid_categories)
            return False, f"Please select one of the following: {categories_str}."
       
        return True, ""
   
    @staticmethod
    def validate_quantity_on_event(quantity):
        """
        Validate quantity field when focus leaves the field
       
        Args:
            quantity (str): Quantity to validate
           
        Returns:
            tuple: (is_valid, error_message)
        """
        valid, message, _ = add_book.validate_quantity(quantity)
        add_book.field_validation_errors['quantity'] = not valid
        return valid, message
   
    @staticmethod
    def validate_quantity(quantity):
        """
        Validate book quantity
       
        Args:
            quantity (str): Quantity to validate
           
        Returns:
            tuple: (is_valid, error_message, formatted_quantity)
        """
        if not quantity or quantity.strip() == "":
            return False, "Quantity cannot be empty.", ""
       
        # Remove spaces
        quantity = quantity.strip()
       
        # Check if it's a positive integer
        if not quantity.isdigit():
            return False, "Quantity must be a number", ""
       
        # Convert to integer
        quantity_int = int(quantity)
       
        # Check if it's positive
        if quantity_int <= 0:
            return False, "Quantity must be a number", ""
       
        return True, "", quantity_int

class BookEditController:
    def __init__(self, view=None):
        """Initialize the BookEdit controller."""
        self.view = view
        self.book_data = None

        # Initialize controller with this view
        # self.controller = BookEditController(self)

       # Update confirm button command
        if view and hasattr(view, 'buttons') and 'btn_Confirm' in view.buttons:
            view.buttons['btn_Confirm'].config(command=self.update_book)
        
        # Get book data from view if available
        if view and hasattr(view, 'book_data'):
            self.book_data = view.book_data
    
    def search_book(self):
        """Search for a book by ISBN and navigate to edit screen if found."""
        if not hasattr(self.view, 'entries') or 'lnE_ISBN' not in self.view.entries:
            print("Error: ISBN entry field not found")
            return
        
        isbn = self.view.entries['lnE_ISBN'].get().strip()
        
        # Validate ISBN format
        if not isbn.isdigit() or len(isbn) != 13:
            messagebox.showerror("Invalid ISBN", "ISBN must be exactly 13 digits.")
            # Set focus back to ISBN field
            self.view.entries['lnE_ISBN'].focus_set()
            return
        
        # Try to find the book
        book = Book.get_book_by_id(isbn)
        
        if not book:
            messagebox.showerror("Book Not Found", "No book found with this ISBN in the database.")
            # Set focus back to ISBN field
            self.view.entries['lnE_ISBN'].focus_set()
            return
        
        print(f"Book found: {book}")  # Debug print
        
        # Book found, navigate to edit screen
        self.view.root.destroy()
        
        # Create new edit screen with book data
        from tkinter import Tk
        from View.BookManagement.BookManaEditBook1 import BookEdit1App
        edit_root = Tk()
        edit_app = BookEdit1App(edit_root, book_data=book)
        edit_root.mainloop()
    
    def update_book(self):
        """Validate all fields and update book in database"""
        print("Update book method called from controller!")
        
        if not self.view or not self.book_data:
            print("Error: View or book data not available")
            return
        
        # Get all field values from view
        field_values = self.view.get_field_values()
        
        # Validate Title
        title = field_values["title"]
        if not title or len(title) < 2 or len(title) > 255:
            self.view.entries["lnE_Title"].focus_set()
            messagebox.showwarning("Invalid Title", "Title must be between 2 and 255 characters.")
            return
        
        # Validate Author
        author = field_values["author"]
        if not author or len(author) < 2 or len(author) > 100:
            self.view.entries["lnE_Author"].focus_set()
            messagebox.showwarning("Invalid Author", "Author must be between 2 and 100 characters.")
            return
        
        if re.search(r'\d', author):
            self.view.entries["lnE_Author"].focus_set()
            messagebox.showwarning("Invalid Author", "Author name cannot contain numbers.")
            return
        
        if not re.match(r'^[a-zA-ZÀ-ỹ\s\-\.,&]+$', author):
            self.view.entries["lnE_Author"].focus_set()
            messagebox.showwarning("Invalid Author", "Only letters, spaces, hyphens (-), periods (. ), commas (,), and ampersands (&) are allowed.")
            return
        
        if re.search(r'[\-]{2,}|[\. ]{2,}|[,]{2,}|[&]{2,}', author):
            self.view.entries["lnE_Author"].focus_set()
            messagebox.showwarning("Invalid Author", "Special characters (., -, comma, &) cannot appear consecutively.")
            return
        
        # Validate Published Year
        year = field_values["published_year"]
        if not year or not year.isdigit():
            self.view.entries["lnE_PublishedYear"].focus_set()
            messagebox.showwarning("Invalid Year", "Published Year must be a number.")
            return
        
        year_int = int(year)
        current_year = datetime.datetime.now().year
        if year_int < 1440 or year_int > current_year:
            self.view.entries["lnE_PublishedYear"].focus_set()
            messagebox.showwarning("Invalid Year", f"Published Year must be between 1440 and {current_year}.")
            return
        
        # Validate Category
        category = field_values["category"]
        valid_categories = [
            "Fiction", "Non-Fiction", "Mystery", "Science",
            "Fantasy", "History", "Romance", "Biography",
            "Thriller", "Technology"
        ]
        
        if not category or category not in valid_categories:
            self.view.entries["lnE_Category"].focus_set()
            messagebox.showwarning("Invalid Category", f"Category must be one of: {', '.join(valid_categories)}.")
            return
        
        # Validate Quantity
        quantity = field_values["quantity"]
        if not quantity or not quantity.isdigit():
            self.view.entries["lnE_Quantity"].focus_set()
            messagebox.showwarning("Invalid Quantity", "Quantity must be a positive integer.")
            return
        
        quantity_int = int(quantity)
        if quantity_int <= 0:
            self.view.entries["lnE_Quantity"].focus_set()
            messagebox.showwarning("Invalid Quantity", "Quantity must be greater than zero.")
            return
        
        # If all fields are valid, proceed with update
        try:
            # Format data
            formatted_title = re.sub(r'\s+', ' ', title)
            formatted_author = self.format_author_name(author)
            
            # Get original book ID
            book_id = self.book_data[0]  # Original ISBN/book_id (unchanged)
            
            print(f"Updating book: ID={book_id}, title={formatted_title}, author={formatted_author}, year={year_int}, category={category}, quantity={quantity_int}")
            
            # Create dictionary with updated data
            updated_data = {
                'title': formatted_title,
                'author': formatted_author,
                'published_year': year_int,
                'category': category,
                'quantity': quantity_int
            }
            
            # Update book in database
            book = Book(book_id=book_id)
            success = book.update_book(updated_data)
            
            print(f"Database update result: {success}")
            
            if success:
                # Show success message using notification system
                from View.noti_tab_view_1 import Message_2
                Message_2(self.view.root, 'edit_book')
            else:
                messagebox.showerror("Update Failed", "Failed to update book information in the database.")
            
        except Exception as e:
            print(f"Error updating book: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Update Error", f"An error occurred: {str(e)}")
    
    def format_author_name(self, author):
        """Format author name with proper capitalization"""
        # Split by spaces
        words = author.split()
        result = []
        
        for word in words:
            # If word contains special characters like period or hyphen
            if '.' in word or '-' in word or ',' in word or '&' in word:
                # Split by special characters and keep them
                parts = []
                current = ""
                for char in word:
                    if char in '.-,&':
                        if current:
                            parts.append(current)
                            current = ""
                        parts.append(char)
                    else:
                        current += char
                if current:
                    parts.append(current)
                
                # Process each part
                processed_parts = []
                for i, part in enumerate(parts):
                    if part in '.-,&':
                        processed_parts.append(part)
                    elif i == 0 or parts[i-1] in '.-':
                        # Capitalize if it's the first part or follows a period or hyphen
                        processed_parts.append(part[0].upper() + part[1:].lower() if part else "")
                    else:
                        # Otherwise lowercase
                        processed_parts.append(part.lower())
                
                result.append(''.join(processed_parts))
            else:
                # Regular word - capitalize first letter
                result.append(word[0].upper() + word[1:].lower() if word else "")
        
        # Join with spaces and standardize multiple spaces
        formatted_author = ' '.join(result)
        return re.sub(r'\s+', ' ', formatted_author)
    
    def validate_title(self, event):
        """Validate title field"""
        title = self.view.entries["lnE_Title"].get().strip()
        
        # Check if empty
        if not title:
            # Only show message if no skip_message flag
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Title", "Title cannot be empty.")
                event.widget._shown_warning = True
            return False
        
        # Check length
        if len(title) < 2 or len(title) > 255:
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Title", "Title must be between 2 and 255 characters.")
                event.widget._shown_warning = True
            return False
        
        # Standardize spaces
        standardized_title = re.sub(r'\s+', ' ', title)
        self.view.entries["lnE_Title"].delete(0, 'end')
        self.view.entries["lnE_Title"].insert(0, standardized_title)
        
        return True
    
    def validate_author(self, event):
        """Validate author field"""
        author = self.view.entries["lnE_Author"].get().strip()
        
        # Check if empty
        if not author:
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", "Author cannot be empty.")
                event.widget._shown_warning = True
            return False
        
        # Check length
        if len(author) < 2 or len(author) > 100:
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", "Author must be between 2 and 100 characters.")
                event.widget._shown_warning = True
            return False
        
        # Check for numbers
        if re.search(r'\d', author):
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", "Author name cannot contain numbers.")
                event.widget._shown_warning = True
            return False
        
        # Check for allowed characters
        if not re.match(r'^[a-zA-ZÀ-ỹ\s\-\.,&]+$', author):
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", "Only letters, spaces, hyphens (-), periods (. ), commas (,), and ampersands (&) are allowed.")
                event.widget._shown_warning = True
            return False
        
        # Check for consecutive special characters
        if re.search(r'[\-]{2,}|[\. ]{2,}|[,]{2,}|[&]{2,}', author):
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", "Special characters (., -, comma, &) cannot appear consecutively.")
                event.widget._shown_warning = True
            return False
        
        # Format author name to title case with special handling
        formatted_author = self.format_author_name(author)
        self.view.entries["lnE_Author"].delete(0, 'end')
        self.view.entries["lnE_Author"].insert(0, formatted_author)
        
        return True
    
    def validate_published_year(self, event):
        """Validate published year field"""
        year = self.view.entries["lnE_PublishedYear"].get().strip()
        
        # Check if empty
        if not year:
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Year", "Published Year cannot be empty.")
                event.widget._shown_warning = True
            return False
        
        # Check if it's a number
        if not year.isdigit():
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Year", "Published Year must be a number.")
                event.widget._shown_warning = True
            return False
        
        # Check range
        year_int = int(year)
        current_year = datetime.datetime.now().year
        
        if year_int < 1440 or year_int > current_year:
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Year", f"Published Year must be between 1440 and {current_year}.")
                event.widget._shown_warning = True
            return False
        
        return True
    
    def validate_category(self, event):
        """Validate category field"""
        category = self.view.entries["lnE_Category"].get().strip()
        
        # Check if empty
        if not category:
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Category", "Category cannot be empty.")
                event.widget._shown_warning = True
            return False
        
        # Valid categories list
        valid_categories = [
            "Fiction", "Non-Fiction", "Mystery", "Science",
            "Fantasy", "History", "Romance", "Biography",
            "Thriller", "Technology"
        ]
        
        # Check if category is valid
        if category not in valid_categories:
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Category", f"Category must be one of: {', '.join(valid_categories)}.")
                event.widget._shown_warning = True
            return False
        
        return True
    
    def validate_quantity(self, event):
        """Validate quantity field"""
        quantity = self.view.entries["lnE_Quantity"].get().strip()
        
        # Check if empty
        if not quantity:
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Quantity", "Quantity cannot be empty.")
                event.widget._shown_warning = True
            return False
        
        # Check if it's a number
        if not quantity.isdigit():
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Quantity", "Quantity must be a positive integer.")
                event.widget._shown_warning = True
            return False
        
        # Check if it's positive
        quantity_int = int(quantity)
        if quantity_int <= 0:
            if not hasattr(event, 'skip_message') and not event.widget._shown_warning:
                messagebox.showwarning("Invalid Quantity", "Quantity must be greater than zero.")
                event.widget._shown_warning = True
            return False
        
        return True
    