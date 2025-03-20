from Model.book_model import Book
from Model.admin_model import Admin
from View.noti_tab_view_1 import Delete, Message_1

class BookManagementController:
    from Model.book_model import Book
from Model.admin_model import Admin
from View.noti_tab_view_1 import Delete, Message_1

class BookManagementController:
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
    
    def on_book_select(self, event):
        """Handle book selection in the table"""
        selected_items = self.view.tbl_Book.selection()
        if selected_items:
            # Get the book ID from the selected row
            item = self.view.tbl_Book.item(selected_items[0])
            self.selected_book_id = item["values"][0]  # First column is book_id
        else:
            self.selected_book_id = None
    
    def delete_selected_book(self):
        """Delete the selected book after confirmation"""
        if not self.selected_book_id:
            # No book selected
            return
        
        # Show delete confirmation dialog
        delete_dialog = Delete(self.view.root, "book")
        # Connect the confirmation callback
        delete_dialog.delete_noti.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.confirm_delete_book('no')
        )
        # Set up yes button to call confirm_delete_book with 'yes'
        # You'd need to modify your Delete class to accept a callback function
    
    def confirm_delete_book(self, option):
        """Callback function for the Delete dialog"""
        if option == 'yes':
            # Check if admin instance exists
            if not self.admin:
                print("Error: Admin not set")
                return
            
            # Delete the book from the database
            success = self.admin.delete_book(self.selected_book_id)
            
            if success:
                # Remove the book from the treeview
                selected_items = self.view.tbl_Book.selection()
                if selected_items:
                    self.view.tbl_Book.delete(selected_items[0])
                
                # Show success message
                Message_1(self.view.root, "book")
                self.selected_book_id = None
    
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
    
    # Navigation methods (placeholders - would connect to actual navigation in a real app)
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
        
    # Static methods for handling button clicks from the view
    @staticmethod
    def delete_book_clicked(view_instance):
        """Static method to handle delete book button click from the view"""
        # Find the controller instance
        if hasattr(view_instance, 'controller'):
            controller = view_instance.controller
            controller.delete_selected_book()
        else:
            print("Error: Controller not found")