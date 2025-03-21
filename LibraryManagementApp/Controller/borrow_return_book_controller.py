# Import Lib
from tkinter import Tk, messagebox
from pathlib import Path
import datetime
import sys
import os

# File directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
# Import view classes
from View.BorrowReturnBook.BorrowReturnBook import BorrowReturnApp
from View.BorrowReturnBook.Return1 import Return1App
from View.BorrowReturnBook.Return2 import Return2App
from View.noti_tab_view_1 import Drop_Off, Message_1, Invalid

# Import model classes
from Database.db_lma import Database
from Model.book_model import Book

class ReturnBookController:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.current_view = None
        self.receipt_data = None
        self.initialize_borrow_return_view()

    def initialize_borrow_return_view(self):
        """Initialize the BorrowReturnApp view"""
        if self.current_view:
            self.current_view.root.destroy()
        
        self.current_view = BorrowReturnApp(self.root)
        
        # Override the default button handlers with controller methods
        self.current_view.on_return_book_clicked = self.show_return_book_view
        self.current_view.on_borrow_book_clicked = self.on_borrow_book_clicked
        self.current_view.on_back_to_homepage_clicked = self.on_back_to_homepage_clicked

    def show_return_book_view(self):
        """Switch to Return1 view for receipt ID input"""
        if self.current_view:
            self.current_view.root.destroy()
        
        self.current_view = Return1App(self.root)
        
        # Override the default button handlers with controller methods
        self.current_view.on_search_click = self.search_receipt
        self.current_view.on_return_book_click = self.show_return_book_view  # Allow return to self
        self.current_view.on_borrow_book_click = self.on_borrow_book_clicked
        self.current_view.on_back_to_homepage_click = self.on_back_to_homepage_clicked

    def search_receipt(self):
        """Search for a receipt by ID and show Return2 view if found"""
        # Get receipt ID from the entry field
        receipt_id = self.current_view.lnE_ReceiptID.get().strip()
        
        if not receipt_id:
            # Show invalid input notification if receipt ID is empty
            Invalid(self.root, 'Input')
            return
        
        # Query the database for the receipt
        try:
            self.db.cursor.execute("""
                SELECT r.receipt_id, r.user_id, r.book_id, r.borrow_date, r.due_date, r.return_date, r.status,
                       b.title, b.author, b.category, u.name
                FROM Receipts r
                JOIN Books b ON r.book_id = b.book_id
                JOIN Users u ON r.user_id = u.user_id
                WHERE r.receipt_id = ? AND r.status = 'borrowed'
            """, (receipt_id,))
            
            self.receipt_data = self.db.cursor.fetchone()
            
            if not self.receipt_data:
                # Show message if no receipt found
                Message_1(self.root, 'receipt')
                return
            
            # Show Return2 view with receipt data
            self.show_return_details_view()
            
        except Exception as e:
            print(f"Error searching for receipt: {e}")
            Invalid(self.root, 'Input')

    def show_return_details_view(self):
        """Show Return2 view with receipt details"""
        if self.current_view:
            self.current_view.root.destroy()
        
        self.current_view = Return2App(self.root)
        
        # Override the default button handlers with controller methods
        self.current_view.on_drop_off_click = self.process_book_return
        self.current_view.on_return_book_click = self.show_return_book_view
        self.current_view.on_borrow_book_click = self.on_borrow_book_clicked
        self.current_view.on_back_to_homepage_click = self.on_back_to_homepage_clicked
        
        # Display receipt data in the table
        self.display_receipt_data()

    def display_receipt_data(self):
        """Display receipt data in the Return2 view"""
        if not self.receipt_data:
            return
        
        # Extract data from receipt_data tuple
        receipt_id, user_id, book_id, borrow_date, due_date, return_date, status, title, author, category, user_name = self.receipt_data
        
        # Create table headers
        self.current_view.canvas.create_text(
            435, 190, text="Receipt ID:", fill="black", font=("Arial", 10, "bold"), anchor="w"
        )
        self.current_view.canvas.create_text(
            435, 220, text="User:", fill="black", font=("Arial", 10, "bold"), anchor="w"
        )
        self.current_view.canvas.create_text(
            435, 250, text="Book Title:", fill="black", font=("Arial", 10, "bold"), anchor="w"
        )
        self.current_view.canvas.create_text(
            435, 280, text="Author:", fill="black", font=("Arial", 10, "bold"), anchor="w"
        )
        self.current_view.canvas.create_text(
            435, 310, text="Category:", fill="black", font=("Arial", 10, "bold"), anchor="w"
        )
        self.current_view.canvas.create_text(
            435, 340, text="Borrow Date:", fill="black", font=("Arial", 10, "bold"), anchor="w"
        )
        self.current_view.canvas.create_text(
            435, 370, text="Due Date:", fill="black", font=("Arial", 10, "bold"), anchor="w"
        )
        
        # Display data values
        self.current_view.canvas.create_text(
            580, 190, text=receipt_id, fill="black", font=("Arial", 10), anchor="w"
        )
        self.current_view.canvas.create_text(
            580, 220, text=user_name, fill="black", font=("Arial", 10), anchor="w"
        )
        self.current_view.canvas.create_text(
            580, 250, text=title, fill="black", font=("Arial", 10), anchor="w"
        )
        self.current_view.canvas.create_text(
            580, 280, text=author, fill="black", font=("Arial", 10), anchor="w"
        )
        self.current_view.canvas.create_text(
            580, 310, text=category, fill="black", font=("Arial", 10), anchor="w"
        )
        self.current_view.canvas.create_text(
            580, 340, text=borrow_date, fill="black", font=("Arial", 10), anchor="w"
        )
        self.current_view.canvas.create_text(
            580, 370, text=due_date, fill="black", font=("Arial", 10), anchor="w"
        )
        
        # Calculate if the book is overdue
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        is_overdue = today > due_date if due_date else False
        
        if is_overdue:
            self.current_view.canvas.create_text(
                580, 400, text="OVERDUE", fill="red", font=("Arial", 10, "bold"), anchor="w"
            )

    def process_book_return(self):
        """Process the book return and update the database"""
        if not self.receipt_data:
            return
        
        receipt_id, user_id, book_id, borrow_date, due_date, return_date, status, title, author, category, user_name = self.receipt_data
        
        try:
            # Update receipt status to 'returned' and set return date
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            self.db.cursor.execute("""
                UPDATE Receipts
                SET status = 'returned', return_date = ?
                WHERE receipt_id = ?
            """, (today, receipt_id))
            
            # Increment book quantity by 1
            book_quantity = Book.get_quantity(book_id)
            if book_quantity is not None:
                self.db.cursor.execute("""
                    UPDATE Books
                    SET quantity = quantity + 1
                    WHERE book_id = ?
                """, (book_id,))
            
            self.db.conn.commit()
            
            # Check if the book is overdue
            is_overdue = today > due_date if due_date else False
            
            # Show success notification
            Drop_Off(self.root, 'overdue' if is_overdue else 'ontime')
            
            # Return to the search view
            self.show_return_book_view()
            
        except Exception as e:
            print(f"Error processing book return: {e}")
            self.db.conn.rollback()
            Invalid(self.root, 'Input')

    # Placeholder methods for other navigation buttons
    def on_borrow_book_clicked(self):
        print("Borrow Book clicked - implement switching to borrow book view")
        # Here you would implement switching to the borrow book view
        # This is outside the scope of the current requirements
    
    def on_back_to_homepage_clicked(self):
        print("Back to Homepage clicked - implement switching to homepage")
        # Here you would implement switching to the homepage
        # This is outside the scope of the current requirements

# Entry point
if __name__ == "__main__":
    root = Tk()
    controller = ReturnBookController(root)
    root.mainloop()