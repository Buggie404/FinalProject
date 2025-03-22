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
    def __init__(self, root, message_type):
        # Setup tab
        self.message_2 = Toplevel(root)
        self.message_2.title(" ")
        self.message_2.geometry("300x150")
        self.message_2.resizable(False, False)
        self.message_2.config(bg='white')

        message_2_map = {'pass_reset': "Password Reset Successfully!",
                         'edit_book': "Updated Successfully!",
                         'pay fine': "Fine Paid"}

        # Title Label
        Label(self.message_2, text=message_2_map[message_type], font=("Montserrat", 18, 'bold'), bg='white',
              fg='black').pack(pady=(20, 10))

        # Return Button
        Button(self.message_2, width=13, text="Return", highlightbackground='white', highlightthickness=1,
               command=lambda: self.back_to_subfun()).pack(pady=10)

    # Switch UI to 1st sub-function window
    def back_to_subfun(self):
        self.message_2.destroy()  # -> def từng new window xong gọi tên lại
        # import first_sub_win ở trên
        # parent_window = self.message_2.master
        # new_root = Tk()
        # Lồng if cho từng message_2_type: if m2t == 'pass reset' ->
        # app = first_sub class(new_root)
        # app.mainloop()
        # parent_window.destroy() (ngoài vòng)


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
        invalid_map = {'account': ("Invalid Account", "Please double-check your email and password!"),
                       'quantity': ('Invalid Quantities',
                                    "No. of books borrow need to be larger than zero and lower or equal to Availible quantities"), 
                                    'Input':("Invalid input", "Please double-check your input"),
                                    'search_book': ("Book Not Found", "No books match your search criteria. Please try a different search term.")}

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
    def __init__(self, root, receipt_status):
        # Config Notification tab
        self.root = root
        self.status = receipt_status
        self.delete_noti = Toplevel(root)
        self.delete_noti.title(" ")
        self.delete_noti.geometry("400x200")
        self.delete_noti.resizable(False, False)
        self.delete_noti.config(bg='white')


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
        overdue = ReturnOverdueApp(overdue_root)
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

    def __init__(self, root, book_data=None, quantity=None):
        # Setup tab
        self.root = root
        self.print_receipt = Toplevel(root)
        self.print_receipt.title(" ")
        self.print_receipt.geometry("400x300")
        self.print_receipt.resizable(False, False)
        self.print_receipt.config(bg='white')

        # Import cart
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.append(parent_dir)

        from Controller.test_borrowbook_controller import BorrowingCart
        self.cart = BorrowingCart.get_instance()

        # If we have book data, add it to cart
        if book_data and quantity:
            self.cart.add_item(book_data[0], book_data[1], quantity)

        # Title Label
        Label(self.print_receipt, text="Book Added to Cart!",
              font=('Montserrat', 18, 'bold'), bg='white', fg='black').pack(pady=(20, 10))

        # Show cart items
        self.create_cart_display()

        # Add More Button
        Button(self.print_receipt, width=13, text="Add More Books",
               highlightbackground='white', highlightthickness=1,
               command=self.add_more_books).pack(pady=10)

        # Checkout Button
        Button(self.print_receipt, width=13, text="Complete Borrowing",
               highlightbackground='white', highlightthickness=1,
               command=self.complete_borrowing).pack(pady=10)

        # Cancel Button
        Button(self.print_receipt, width=13, text="Cancel",
               highlightbackground='white', highlightthickness=1,
               command=self.cancel_borrowing).pack(pady=10)

    def create_cart_display(self):
        """Create a display of cart items"""
        # Create frame for cart items
        from tkinter import Frame, Label, Scrollbar

        cart_frame = Frame(self.print_receipt, bg='white')
        cart_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Headers
        Label(cart_frame, text="Book ID", width=15, bg='white', font=('Montserrat', 10, 'bold')).grid(row=0, column=0)
        Label(cart_frame, text="Title", width=25, bg='white', font=('Montserrat', 10, 'bold')).grid(row=0, column=1)
        Label(cart_frame, text="Quantity", width=10, bg='white', font=('Montserrat', 10, 'bold')).grid(row=0, column=2)

        # Item rows
        for i, item in enumerate(self.cart.items):
            Label(cart_frame, text=item['book_id'], width=15, bg='white').grid(row=i + 1, column=0)

            # Truncate title if too long
            title = item['title']
            if len(title) > 20:
                title = title[:17] + "..."

            Label(cart_frame, text=title, width=25, bg='white').grid(row=i + 1, column=1)
            Label(cart_frame, text=str(item['quantity']), width=10, bg='white').grid(row=i + 1, column=2)

    def add_more_books(self):
        """Return to Borrow1 to add more books"""
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

        from Model.receipt_model import Receipt
        from Model.book_model import Book
        from Controller.test_borrowbook_controller import BorrowController

        # Check if borrowing limit would be exceeded
        can_borrow, remaining, total_borrowed = BorrowController.check_borrowing_limit(
            self.cart.user_id, self.cart.get_total_quantity()
        )

        if not can_borrow:
            from tkinter import messagebox
            messagebox.showwarning(
                "Borrowing Limit Exceeded",
                f"You cannot borrow {self.cart.get_total_quantity()} more books.\n"
                f"You currently have {total_borrowed} books borrowed.\n"
                f"Your limit is {BorrowController.MAX_TOTAL_BOOKS} books in total.\n"
                f"You can borrow up to {remaining} more books."
            )
            return

        # Create receipts
        from datetime import datetime, timedelta

        # Calculate borrow date (today) and return date (20 days from today)
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        return_date_str = (today + timedelta(days=20)).strftime('%Y-%m-%d')

        # Create receipt object
        receipt = Receipt(
            user_id=self.cart.user_id,
            borrow_date=today_str,
            return_date=return_date_str,
            status="Borrowed"
        )

        # Save multiple receipts (one for each book)
        success = receipt.save_multi_receipt(self.cart.items)

        if not success:
            from tkinter import messagebox
            messagebox.showerror("Error", "Failed to create receipts. Please try again.")
            return

        # Update book quantities
        for item in self.cart.items:
            book_data = Book.get_book_by_id(item['book_id'])
            current_quantity = book_data[5]
            new_quantity = current_quantity - item['quantity']

            book = Book(book_id=item['book_id'])
            book.update_book({
                'title': book_data[1],
                'author': book_data[2],
                'category': book_data[4],
                'published_year': book_data[3],
                'quantity': new_quantity
            })

        # Clear the cart
        self.cart.clear()

        # Switch to receipt view
        self.print_receipt.destroy()

        # Import BorrowReceiptApp
        from View.BorrowReturnBook.BorrowReceipt import BorrowReceiptApp
        # Close current window
        self.root.destroy()

        # Create new BorrowReceipt window with first receipt_id and borrow date
        new_window = Tk()
        app = BorrowReceiptApp(new_window, receipt_id=receipt.receipt_id, borrow_date=today_str)
        new_window.mainloop()

    def cancel_borrowing(self):
        """Cancel the borrowing process"""
        # Clear the cart
        self.cart.clear()

        # Close the window
        self.print_receipt.destroy()

        # Close current window
        self.root.destroy()

        # Create new Homepage window
        homepage_root = Tk()
        from View.BorrowReturnBook.Borrow1 import Borrow1App
        app = Borrow1App(homepage_root)
        homepage_root.mainloop()