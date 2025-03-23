# Import Lib
from tkinter import *


# Import First_Sub_Win and Current_sub_Win
# from first-sub-win import frst-sub class
# from current-sub-win import current-sub class

class Delete():  # To confirm delection
    def __init__(self, root, delete_type,yes_callback=None):
        """delete_type: 'book' or 'account'
        yes_callback: function to call when 'Yes' is clicked"""

        # Config Notification tab
        self.root = root
        self.delete_type = delete_type
        self.delete_noti = Toplevel(root)
        self.yes_callback = yes_callback

        # Dynamic Title and Messages
        delete_map = {'book': ('Delete Book', "Are you sure you want to delete this book?"),
                      'account': ('Delete Account', "Are you sure you want to delete this account?")}

        # Setup tab
        self.delete_noti.title(" ")
        self.delete_noti.geometry("400x200")
        self.delete_noti.resizable(False, False)
        self.delete_noti.config(bg='white')

        # Title Label
        Label(self.delete_noti, text=delete_map[delete_type][0], font=('Montserrat', 18, 'bold'), bg='white',
              fg='black').pack(pady=(20, 10))
        # Message Label
        Label(self.delete_noti, text=delete_map[delete_type][1], font=("Montserrat", 12), bg='white', fg='black').pack(
            pady=(10, 10))

        # Yes Button
        Button(self.delete_noti, width=13, text="Yes", highlightbackground='white', highlightthickness=1,
               command=lambda: self.choice('yes')).pack(pady=10)
        # No Button
        Button(self.delete_noti, width=13, text="No", highlightbackground='white', highlightthickness=1,
               command=lambda: self.choice('no')).pack(pady=10)
    def set_yes_callback(self, callback):
        """Set the callback function for the 'Yes' button"""
        self.yes_callback = callback
    # Choice function
    def choice(self, option):
        if option == 'yes':  # When clicked 'Yes' button -> switch to notify mess
            # Cho chức năng xoá sách từ Controller vào
            if self.yes_callback:
                self.yes_callback()
            else:
                # Default behavior if no callback is provided
                Message_1(self.root, self.delete_type)
        else:        
            print('Action canceled')
        self.delete_noti.destroy()


class Message_1():  # To notify message (Type 1: When clicked 'OK' button -> messagebox disappear)
    def __init__(self, root, delete_type):
        # Setup tab
        self.message_1 = Toplevel(root)
        self.message_1.title(" ")
        self.message_1.geometry("300x150")
        self.message_1.resizable(False, False)
        self.message_1.config(bg='white')

        self.delete_type = delete_type

        # Dynamic Message
        message_1_map = {'book': "Book Deleted!",
                         'account': "Account Deleted!",
                         'edit_pass_id': 'No match ID!',
                         'edit_book_id': "No match ISBN!",
                         'receipt': "No match receipt ID!",
                         'search_account': 'No match User!',
                         'search_book': 'No match book!'}

        # Tile Label
        Label(self.message_1, text=message_1_map[delete_type], font=("Montserrat", 18, 'bold'), bg='white',
              fg='black').pack(pady=(20, 10))

        # OK Button
        Button(self.message_1, width=13, text="OK", highlightbackground='white', highlightthickness=1,
               command=self.message_1.destroy).pack(pady=10)


class Message_2():  # To notify message (Type 2: when clicked 'Return' button -> switch back to the first frame of sub-function)
    def __init__(self, root, message_type = None):
        # Setup tab
        self.message_2 = Toplevel(root)
        self.message_type = message_type
        self.message_2.title(" ")
        self.message_2.geometry("350x150+0+0")
        self.message_2.resizable(False, False)
        self.message_2.config(bg='white')

        # Lưu message_type vào biến instance
        self.message_type = message_type

        message_2_map = {'pass_reset': "Password Reset Successfully!",
                         'edit_book': "Updated Successfully!",
                         'pay_fine': "Fine Paid"}

        # Title Label
        Label(self.message_2, text=message_2_map[message_type], font=("Montserrat", 18, 'bold'), bg='white',
              fg='black').pack(pady=(20, 10))

        # Return Button
        Button(self.message_2, width=13, text="Return", highlightbackground='white', highlightthickness=1,
               command=lambda: self.back_to_subfun()).pack(pady=10)

    # Switch UI to 1st sub-function window
    def back_to_subfun(self):
        self.message_2.destroy() 
        if self.message_type == 'edit_book':
            # Đóng màn hình hiện tại
            parent_window = self.message_2.master
            parent_window.destroy()
        
            # Open BookManagement screen
            from View.BookManagement.BookManagement import BookManagementApp
            management_root = Tk()
            management_app = BookManagementApp(management_root)
            management_root.mainloop()
        
        if self.message_type == 'pass_reset':
            # Đóng màn hình hiện tại
            parent_window = self.message_2.master
            parent_window.destroy()

            # Mở màn hình UserEditAccount
            from View.UserManagement.UserEditAccount import UserEditAccountApp
            reset_pass_root = Tk()
            reset_pass = UserEditAccountApp(reset_pass_root)
            reset_pass_root.mainloop()

        else: # pay_fine
            # Will be handle by ReturnOverdue
            pass    
        

class Invalid():  # To notify Invalid input  # nhớ thêm Invalid user Id format
    def __init__(self, root, invalid_type):
        # Setup tab
        self.root = root
        self.invalid_type = invalid_type
        self.invalid = Toplevel(root)
        self.invalid.title(" ")
        self.invalid.geometry("400x200")
        self.invalid.resizable(False, False)
        self.invalid.config(bg='white')

        # Dynamic Title and Message
        invalid_map = {
    'account': ("Invalid Account", "Please double-check your email and password! "),
    'quantity': ('Invalid Quantities', "No. of books borrow need to be larger than zero and lower or equal to Available quantities"),
    'Input': ("Invalid input", "Please double-check your input"),
    'search_book': ("Book Not Found", "No books match your search criteria. Please try a different search term."),
    'borrowing_limit': ("Borrowing Limit Exceeded", "You have reached your borrowing limit. Please return some books before borrowing more.")
}

        # Title Label
        Label(self.invalid, text=invalid_map[invalid_type][0], font=("Montserrat", 18, 'bold'), bg='white',
              fg='black').pack(pady=(20, 10))
        # Message Label
        Label(self.invalid, text=invalid_map[invalid_type][1], font=("Montserrat", 12), bg='white', fg='black').pack(
            pady=(10, 10))

        # Ok button
        Button(self.invalid, width=13, text="OK", highlightbackground='white', highlightthickness=1,
               command=lambda: self.invalid.destroy()).pack(pady=10)


class Drop_Off():
    def __init__(self, root, receipt_status, receipt_id=None):
        # Config Notification tab
        self.root = root
        self.status = receipt_status
        self.delete_noti = Toplevel(root)
        self.delete_noti.title(" ")
        self.delete_noti.geometry("400x200")
        self.delete_noti.resizable(False, False)
        self.delete_noti.config(bg='white')
        self.receipt_id = receipt_id 

        # Title Label
        Label(self.delete_noti, text="Drop Off Successfully!", font=('Montserrat', 18, 'bold'), bg='white',
              fg='black').pack(pady=(20, 10))
        
        # Notification Button based on receipt staus
        if self.status == "Overdue":
            # Pay Overdue Fine
            Button(self.delete_noti, width=13, text="Pay Overdue Fine", highlightbackground='white', highlightthickness=1, command = lambda: self.pay_overdue_fine()).pack(pady=10)
        else: 
            # Return Button
            Button(self.delete_noti, width=13, text="Return to Home", highlightbackground='white', highlightthickness=1, command = lambda: self.switch_to_return()).pack(pady=10)
        
    # Switch to Return Book Window
    def switch_to_return(self):
        self.delete_noti.destroy()
        self.root.destroy()
        from View.BorrowReturnBook.Return1 import Return1App
        return_1_root = Tk()
        return_1 = Return1App(return_1_root)
        return_1_root.mainloop()
        
    # Switch to Overdue Window
    def pay_overdue_fine(self):
        self.delete_noti.destroy()
        self.root.destroy()
        from View.BorrowReturnBook.ReturnOverdue import ReturnOverdueApp
        overdue_root = Tk()
        overdue = ReturnOverdueApp(overdue_root, receipt_id = self.receipt_id)
        overdue_root.mainloop()


class Sign_Out():  # To Sign out, when clicked "Yes" -> switch to Log_In window
    def __init__(self, root):
        # Setup tab
        self.root = root
        self.sign_out = Toplevel(root)
        self.sign_out.title(" ")
        self.sign_out.geometry("400x200")
        self.sign_out.resizable(False, False)
        self.sign_out.config(bg='white')

        # Title Label
        Label(self.sign_out, text="Sign Out", font=('Montserrat', 18, 'bold'), bg='white', fg='black').pack(
            pady=(20, 10))
        # Message Label
        Label(self.sign_out, text="Are you sure you want to sign out?", font=("Montserrat", 12), bg='white',
              fg='black').pack(pady=(10, 10))

        # Yes Button
        Button(self.sign_out, width=13, text="Yes", highlightbackground='white', highlightthickness=1,
               command=lambda: self.switch_to_log_in()).pack(pady=(10, 10))
        # No Button
        Button(self.sign_out, width=13, text="No", highlightbackground='white', highlightthickness=1,
               command=lambda: self.sign_out.destroy()).pack(pady=(10, 10))

    def switch_to_log_in(self):
        # Only import here so that it would crash if LogIn file also imported this file
        from LogIn import LogInApp
        self.sign_out.destroy()  # Close the Sign_Out window
        self.root.destroy()  # Close the main root

        # Create a new root for LogIn
        log_in_root = Tk()
        LogInApp(log_in_root) 
        log_in_root.mainloop()

class Print_Receipt():
    """To manage the borrowing cart and finalize the transaction"""

    def __init__(self, root, user_data=None, book_data=None, quantity=None):
        # Setup tab
        self.root = root
        self.user_data = user_data
        self.print_receipt = Toplevel(root)
        self.print_receipt.title("Borrowing Cart")

        # Expanded geometry to fit all content
        self.print_receipt.geometry("500x500")
        self.print_receipt.resizable(False, False)
        self.print_receipt.config(bg='white')

        # Ensure print_receipt window stays on top
        self.print_receipt.transient(root)
        self.print_receipt.grab_set()

        # Import cart
        import sys
        import os
        from tkinter import Frame, Label, Button, Scrollbar

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.append(parent_dir)

        from Controller.test_borrowbook_controller import BorrowingCart

        self.cart = BorrowingCart.get_instance()

        # If we have book data, add it to cart
        if book_data and quantity:
            print(f"Adding to cart: {book_data[0]}, {book_data[1]}, qty: {quantity}")
            self.cart.add_item(book_data[0], book_data[1], quantity)

        # Title Label
        title_label = Label(
            self.print_receipt,
            text="Book Added to Cart! ",
            font=('Montserrat', 18, 'bold'),
            bg='white',
            fg='black'
        )
        title_label.pack(pady=(20, 10))

        # Debug print cart contents
        self.cart.print_contents()

        # Create a frame for cart items with scrollbar
        cart_container = Frame(self.print_receipt, bg='white')
        cart_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Add scrollbar for many items
        scrollbar = Scrollbar(cart_container)
        scrollbar.pack(side='right', fill='y')

        # Create inner frame for cart items
        cart_frame = Frame(cart_container, bg='white')
        cart_frame.pack(fill='both', expand=True)

        # Configure scrollbar
        # Note: This is simplified - for a real scrollable area you might need a Canvas

        # Headers
        Label(cart_frame, text="Book ID", width=12, bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5, pady=5)
        Label(cart_frame, text="Title", width=25, bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=5, pady=5)
        Label(cart_frame, text="Quantity", width=8, bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=5, pady=5)

        # Item rows
        for i, item in enumerate(self.cart.items):
            Label(cart_frame, text=item['book_id'], width=12, bg='white').grid(row=i + 1, column=0, padx=5, pady=3)

            # Truncate title if too long
            title = item['title']
            if len(title) > 20:
                title = title[:17] + "..."

            Label(cart_frame, text=title, width=25, bg='white').grid(row=i + 1, column=1, padx=5, pady=3)
            Label(cart_frame, text=str(item['quantity']), width=8, bg='white').grid(row=i + 1, column=2, padx=5, pady=3)

        # Create a frame for buttons
        button_frame = Frame(self.print_receipt, bg='white')
        button_frame.pack(fill='x', padx=20, pady=20)

        # Add More Button - using standard tkinter button settings
        self.add_more_btn = Button(
            button_frame,
            text="Add More Books",
            width=15,
            height=2,
            bg='#f0f0f0',
            activebackground='#e0e0e0',
            command=self.add_more_books
        )
        self.add_more_btn.pack(side='left', padx=10)

        # Checkout Button
        self.checkout_btn = Button(
            button_frame,
            text="Complete Borrowing",
            width=15,
            height=2,
            bg='#f0f0f0',
            activebackground='#e0e0e0',
            command=self.complete_borrowing
        )
        self.checkout_btn.pack(side='left', padx=10)

        # Cancel Button
        self.cancel_btn = Button(
            button_frame,
            text="Cancel",
            width=15,
            height=2,
            bg='#f0f0f0',
            activebackground='#e0e0e0',
            command=self.cancel_borrowing
        )
        self.cancel_btn.pack(side='left', padx=10)

        # Debug print
        print(f"Print_Receipt initialized with cart containing {len(self.cart.items)} items")

    def add_more_books(self):
        """Return to Borrow1 to add more books"""
        print("Add more books clicked")
        self.print_receipt.destroy()

        # Import Borrow1App
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.append(parent_dir)
        from View.BorrowReturnBook.Borrow1 import Borrow1App
        from tkinter import Tk

        # Close current window
        self.root.destroy()

        # Create new Borrow1 window
        new_window = Tk()
        
        # Pass the user_id from the cart
        user_data = None
        if self.cart.user_id:
            user_data = (self.cart.user_id,)
            
        app = Borrow1App(new_window, user_data=user_data)
        new_window.mainloop()

    def complete_borrowing(self):
        """Complete the borrowing process and create receipts"""
        print("Complete borrowing clicked")
        if self.cart.is_empty():
            from tkinter import messagebox
            messagebox.showinfo("Empty Cart", "Your borrowing cart is empty.")
            return

        # Import required modules
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.append(parent_dir)
        from Controller.test_borrowbook_controller import BorrowController
        from View.BorrowReturnBook.BorrowReceipt import BorrowReceiptApp
        from tkinter import Tk, messagebox

        # Check if we have a valid user_id
        if not self.cart.user_id:
            messagebox.showerror("Error", "No user ID associated with this cart.")
            return

        # Print cart contents before completing
        self.cart.print_contents()

        # Use the controller to complete the borrowing process
        try:
            success, receipt_id, borrow_date, return_deadline = BorrowController.complete_borrowing(
                self.cart.user_id, 
                self.cart.items
            )

            if not success:
                messagebox.showerror("Error", "Failed to create receipts. Please try again.")
                return

            print(f"Successfully completed borrowing with receipt ID: {receipt_id}")

            # Clear the cart
            self.cart.clear()

            # Switch to receipt view
            self.print_receipt.destroy()
            self.root.destroy()

            # Create new BorrowReceipt window with receipt_id, borrow date, and return deadline
            new_window = Tk()
            app = BorrowReceiptApp(
                new_window, 
                user_data = self.user_data,
                receipt_id=receipt_id, 
                borrow_date=borrow_date,
                return_deadline=return_deadline
            )
            new_window.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(f"Error in complete_borrowing: {e}")
            import traceback
            traceback.print_exc()

    def cancel_borrowing(self):
        """Cancel the borrowing process"""
        print("Cancel borrowing clicked")
        
        # Clear the cart
        self.cart.clear()
        
        # Close the print receipt window
        self.print_receipt.destroy()
        
        # Close current window
        self.root.destroy()
        
        # Create new Homepage window
        from tkinter import Tk
        borrow_root = Tk()
        
        try:
            # Try to import BorrowReturnApp - adjust the import path if needed
            from View.BorrowReturnBook.BorrowReturnBook import BorrowReturnApp
            app = BorrowReturnApp(borrow_root)
        except ImportError:
            # Fallback to Borrow1 if BorrowReturnApp is not found
            from View.BorrowReturnBook.Borrow1 import Borrow1App
            app = Borrow1App(borrow_root)
            
        borrow_root.mainloop()
    
class AlreadyReturnedNotification():
    def __init__(self, root, message="This book has already been returned!"):
        # Setup tab
        self.root = root
        self.notification = Toplevel(root)
        self.notification.title(" ")
        self.notification.geometry("400x200")
        self.notification.resizable(False, False)
        self.notification.config(bg='white')
        invalid_map = {
             'return_status_error': ("Already Returned", "This book has already been returned or marked as overdue. You cannot return it again.")}
        # Title Label
        Label(self.notification, text="Already Returned", font=('Montserrat', 18, 'bold'), bg='white', fg='black').pack(pady=(20, 10))
        # Message Label
        Label(self.notification, text=message, font=("Montserrat", 12), bg='white', fg='black').pack(pady=(10, 10))

        # OK Button
        Button(self.notification, width=13, text="OK", highlightbackground='white', highlightthickness=1, 
               command=self.notification.destroy).pack(pady=10)
