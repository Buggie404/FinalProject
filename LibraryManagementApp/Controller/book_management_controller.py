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

# from View.BookManaAddBook import BookManagementAddBookApp
# from View.BookManaAddBook1 import BookManaAddBook1App

class DeleteBook:
    def __init__(self, view):
        """
        Initialize the Book Management Controller.
        
        Args:
            view: The BookManagementApp view instance
        """
        self.view = view
        self.admin = None
        self.selected_book_id = None
        
        # Bind events to UI elements
        self.bind_events()
    
    def bind_events(self):
        """Bind events to UI elements"""
        # Bind the delete book button
        self.view.buttons["btn_DeleteBook"].config(command=self.delete_selected_book)
        
        # Bind select event for the book table
        self.view.tbl_Book.bind("<<TreeviewSelect>>", self.on_book_select)
        
        # Bind category filter buttons
        self.view.buttons["btn_Fantasy"].config(command=lambda: self.filter_by_category("Fantasy"))
        self.view.buttons["btn_Fiction"].config(command=lambda: self.filter_by_category("Fiction"))
        self.view.buttons["btn_Romance"].config(command=lambda: self.filter_by_category("Romance"))
        self.view.buttons["btn_Technology"].config(command=lambda: self.filter_by_category("Technology"))
        self.view.buttons["btn_Biography"].config(command=lambda: self.filter_by_category("Biography"))
        
        # Bind search entry
        self.view.entries["lnE_SearchBook"].bind("<Return>", self.search_books)
        
        # Bind navigation buttons
        self.view.buttons["btn_AddBook"].config(command=self.navigate_to_add_book)
        self.view.buttons["btn_EditBookInformation"].config(command=self.navigate_to_edit_book)
        self.view.buttons["btn_BackToHomepage"].config(command=self.navigate_to_homepage)
    
    def set_admin(self, admin):
        """Set the admin user for performing admin operations"""
        self.admin = admin
    
    # def on_book_select(self, event):
    #     """Handle book selection in the table"""
    #     selected_items = self.view.tbl_Book.selection()
    #     if selected_items:
    #         # Get the book ID from the selected row
    #         item = self.view.tbl_Book.item(selected_items[0])
    #         self.selected_book_id = item["values"][0]  # First column is book_id
    #         print(f"Selected book ID: {self.selected_book_id}")
    #     else:
    #         self.selected_book_id = None
    def on_book_select(self, event):
        """Handle book selection in the table"""
        selected_items = self.view.tbl_Book.selection()
        if selected_items:
            # Get the book ID from the selected row
            item = self.view.tbl_Book.item(selected_items[0])
            
            # Get the book_id and ensure it has 10 digits with leading zeros
            raw_book_id = str(item["values"][0])
            self.selected_book_id = raw_book_id.zfill(10)  # Pad with leading zeros to make 10 digits
            
            print(f"Selected book ID: {self.selected_book_id}")
        else:
            self.selected_book_id = None

    
    def delete_selected_book(self):
        """Show delete confirmation dialog and handle deletion"""
        if not self.selected_book_id:
            print("❌ No book selected.")
            return

        print(f"🗑️ Attempting to delete book ID: {self.selected_book_id}")
        
        # Create delete confirmation dialog
        delete_dialog = Delete(self.view.root, "book")
        
        # Set callback for Yes button
        delete_dialog.set_yes_callback(self.confirm_delete_book)
    
    # def confirm_delete_book(self):
    # #Delete the selected book from database and UI
    #     if not self.admin:
    #         print("❌ Admin not set")
    #         return
    #     # Store the selected book ID locally in case selection changes
    #     book_id_to_delete = self.selected_book_id
        
    #     # Get the selected item from the treeview BEFORE deleting from database
    #     selected_items = self.view.tbl_Book.selection()
    #     selected_item = selected_items[0] if selected_items else None
        
    #     if not selected_item:
    #         print("❌ No item selected in the table")
    #         return
        
    #     # Delete book from database
    #     success = self.admin.delete_book(book_id_to_delete)
        
    #     if success:
    #         print(f"✅ Successfully deleted book ID: {book_id_to_delete}")
            
    #         # Remove book directly from UI table using the selected item
    #         self.view.tbl_Book.delete(selected_item)
            
    #         # Show success message
    #         Message_1(self.view.root, "book")
            
    #         # Reset selected book ID
    #         self.selected_book_id = None
    #     else:
    #         print("❌ Failed to delete book from database")
    def confirm_delete_book(self):
        #Delete the selected book from database and UI
        if not self.admin:
            print("❌ Admin not set")
            return
            
        # Store the selected book ID locally in case selection changes
        book_id_to_delete = self.selected_book_id
        
        # Get the selected item from the treeview BEFORE deleting from database
        selected_items = self.view.tbl_Book.selection()
        selected_item = selected_items[0] if selected_items else None
        
        if not selected_item:
            print("❌ No item selected in the table")
            return
        
        # Ensure book_id has 10 digits with leading zeros
        book_id_to_delete = str(book_id_to_delete).zfill(10)
        
        # Delete book from database
        success = self.admin.delete_book(book_id_to_delete)
        
        if success:
            print(f"✅ Successfully deleted book ID: {book_id_to_delete}")
            
            # Remove book directly from UI table using the selected item
            self.view.tbl_Book.delete(selected_item)
            
            # Show success message
            Message_1(self.view.root, "book")
            
            # Reset selected book ID
            self.selected_book_id = None
        else:
            print("❌ Failed to delete book from database")
            # Use a standard message type instead of a custom one
            Invalid(self.view.root, "input")  # Using "input" as the type since it's likely defined


    
    def filter_by_category(self, category):
        """Filter books by category"""
        # Clear current table
        for item in self.view.tbl_Book.get_children():
            self.view.tbl_Book.delete(item)
        
        # Fetch books by category
        books = Book.get_book_by_category(category)
        
        # Populate table with filtered books
        if books:
            for book in books:
                self.view.tbl_Book.insert('', 'end', values=(
                    book[0],  # book_id
                    book[1],  # title
                    book[2],  # author
                    book[3],  # published_year
                    book[4],  # category
                    book[5]   # quantity
                ))
    
    def search_books(self, event=None):
        """Search books by title"""
        search_term = self.view.entries["lnE_SearchBook"].get()
        
        # Skip search if the text is the placeholder
        if search_term == "Search":
            return
        
        # Clear current table
        for item in self.view.tbl_Book.get_children():
            self.view.tbl_Book.delete(item)
        
        # Fetch books matching the search term
        books = Book.search_books(search_term)
        
        # Populate table with search results
        if books:
            for book in books:
                self.view.tbl_Book.insert('', 'end', values=(
                    book[0],  # book_id
                    book[1],  # title
                    book[2],  # author
                    book[3],  # published_year
                    book[4],  # category
                    book[5]   # quantity
                ))
    
    def refresh_book_table(self):
        """Refresh the book table with all books"""
        # Clear current table
        for item in self.view.tbl_Book.get_children():
            self.view.tbl_Book.delete(item)
        
        # Load all books
        books = Book.get_all_book()
        
        if books:
            for book in books:
                self.view.tbl_Book.insert('', 'end', values=(
                    book[0],  # book_id
                    book[1],  # title
                    book[2],  # author
                    book[3],  # published_year
                    book[4],  # category
                    book[5]   # quantity
                ))
    
    # Navigation methods
    def navigate_to_add_book(self):
        """Navigate to Add Book screen"""
        print("Navigating to Add Book screen")
        # Implementation would depend on your app's navigation structure
    
    def navigate_to_edit_book(self):
        """Navigate to Edit Book screen"""
        print("Navigating to Edit Book screen")
        # Implementation would depend on your app's navigation structure
    
    def navigate_to_homepage(self):
        """Navigate back to homepage"""
        print("Navigating to Homepage")
        # Implementation would depend on your app's navigation structure

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
        Validate that ISBN contains only positive integers, no spaces, no leading zeros
        
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
            return False, "ISBN must be a positive integer, no spaces."
        #Check for exactly 10 digits
        if len(isbn) != 10:
            return False, "ISBN must be exactly 10 digits long."
        # Check for leading zeros
        # if isbn.startswith('0'):
        #     return False, "ISBN must be a positive integer, no spaces, no leading zeros."
        
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
    
    # @staticmethod
    # def validate_title(title):
    #     """
    #     Validate book title
        
    #     Args:
    #         title (str): Title to validate
            
    #     Returns:
    #         tuple: (is_valid, error_message, formatted_title)
    #     """
    #     if not title or title.strip() == "":
    #         return False, "Title cannot be empty.", ""
        
    #     # Check length
    #     if len(title.strip()) < 2:
    #         return False, "Length: 2 to 255 characters.", ""
    #     if len(title.strip()) > 255:
    #         return False, "Length: 2 to 255 characters.", ""
        
    #     # Remove extra spaces at beginning and end
    #     formatted_title = title.strip()
        
    #     # Standardize multiple spaces to single space
    #     formatted_title = re.sub(r'\s+', ' ', formatted_title)
        
    #     # Check for invalid special characters
    #     allowed_pattern = r'^[a-zA-Z0-9\s\-_.,:"\'!?]+$'
    #     if not re.match(allowed_pattern, formatted_title):
    #         return False, "Special characters (@, #, $, %, *, etc.) are not allowed.", ""
        
    #     return True, "", formatted_title
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
        
        # Define allowed characters (after conversion to ASCII)
        # Allow letters, numbers, spaces, basic punctuation
        allowed_pattern = r'^[a-zA-Z0-9\s\-_.,:"\'!?]+$'
        if not re.match(allowed_pattern, ascii_title):
            return False, "Special characters (@, #, $, %, *, etc.) are not allowed.", ""
        
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
    
    # @staticmethod
    # def validate_author(author):
    #     """
    #     Validate book author
        
    #     Args:
    #         author (str): Author to validate
            
    #     Returns:
    #         tuple: (is_valid, error_message, formatted_author)
    #     """
    #     if not author or author.strip() == "":
    #         return False, "Author cannot be empty.", ""
        
    #     # Check length
    #     if len(author.strip()) < 2:
    #         return False, "Length: 2 to 100 characters.", ""
    #     if len(author.strip()) > 100:
    #         return False, "Length: 2 to 100 characters.", ""
        
    #     # Remove extra spaces at beginning and end
    #     author = author.strip()
        
    #     # Check for numbers
    #     if re.search(r'\d', author):
    #         return False, "Special characters (@, #, $, %, *, etc.) and numbers are not allowed.", ""
        
    #     # Check for allowed characters
    #     allowed_pattern = r'^[a-zA-Z\s\-\.]+$'
    #     if not re.match(allowed_pattern, author):
    #         return False, "Only letters, spaces, hyphens (-), and periods (.) are allowed.", ""
        
    #     # Convert to Title Case
    #     formatted_author = ' '.join(word.capitalize() for word in author.split())
        
    #     return True, "", formatted_author
    
    @staticmethod
    def validate_author(author):
        """
        Validate book author with support for Vietnamese characters
        
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
        allowed_pattern = r'^[a-zA-Z\s\-\.]+$'
        if not re.match(allowed_pattern, ascii_author):
            return False, "Only letters, spaces, hyphens (-), and periods (.) are allowed.", ""
        
        # Convert to Title Case (properly handling Vietnamese)
        # First convert to lowercase then capitalize each word
        words = author.lower().split()
        formatted_author = ' '.join(word[0].upper() + word[1:] for word in words)
        
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
            return False, "Please enter a positive integer between 1440 and the current year.", ""
        
        # Convert to integer
        year_int = int(year)
        current_year = datetime.datetime.now().year
        
        # Check range
        if year_int < 1440 or year_int > current_year:
            return False, f"Please enter a positive integer between 1440 and {current_year}.", ""
        
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
            return False, "Quantity must be a positive integer", ""
        
        # Convert to integer
        quantity_int = int(quantity)
        
        # Check if it's positive
        if quantity_int <= 0:
            return False, "Quantity must be a positive integer", ""
        
        return True, "", quantity_int
