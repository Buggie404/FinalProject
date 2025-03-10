"""File hiện UI, chưa thêm function cơ bản, chưa cho switch giữa các window"""
# Import Lib
from tkinter import *
# import function_controller

class Delete(): # To confirm deletion (Delete Book, Delete Account)
    def __init__(self, root, delete_type): 
        """delete_type: 'book' or 'account to determine UI'"""
        self.root = root
        self.delete_type = delete_type
        self.delete_noti = Toplevel(root)

        #Dynamic Title and Messages
        title_map = {'book': ("Delete Book", "Are you sure you want to delete this book?"),
                     'account': ("Delete Account", "Are you sure you want to delete this account?")}
        
        # Setup notification tab
        self.delete_noti.title(" ")
        self.delete_noti.geometry("400x200")
        self.delete_noti.resizable(False, False)
        self.delete_noti.config(bg = 'white')

        #Title Label
        Label(self.delete_noti, text = title_map[delete_type][0], font = ('Arial', 18, 'bold'), bg = 'white', fg = 'black').pack(pady = (20,10))
        # Message Label
        Label(self.delete_noti, text = title_map[delete_type][1], font = ('Arial', 12), bg = 'white', fg= 'black').pack(pady = (10,10))

        # Yes button
        Button(self.delete_noti, width = 13, text = 'Yes', highlightbackground = 'white', highlightthickness = 1, command = lambda: self.choice('yes')).pack(pady = 10)
        # No button
        Button(self.delete_noti, width = 13, text = 'No', highlightbackground = 'white', highlightthickness = 1, command = lambda: self.choice('no')).pack(pady = 10)

    def choice(self, option):
        if option == 'yes':
            print(f"{self.delete_type.capitalize()} actio confirmed") # Thế bằng action từ Controller
            Message(self.root, self.delete_type)
        else:
            print('Action canceled')
        self.delete_noti.destroy()

class Message(): # To notify message (Book Deleted!, Fine Paid!)
    def __init__(self, root, delete_type):
        """delete_type: 'book' or 'account' to determine success message"""
        # Setup tab
        self.message = Toplevel(root)
        self.message.title(" ")
        self.message.geometry("300x150")
        self.message.resizable(False, False)
        self.message.config(bg = 'white')

        # Dynamic Success Message
        success_map = {'book': "Book Deleted!", 
                       'account': "Account Deleted!",
                       'find_receipt': "Receipt ID not Found!",
                       'find_book': "No match ISBN!",
                       "find_account": "No match ID!"}
        
        #Title Label
        Label(self.message, text = success_map[delete_type], font = ('Arial', 18, 'bold'), bg = 'white', fg = 'black').pack(pady = (20,10))

        # OK button
        Button(self.message, width = 13, text = 'OK', highlightbackground = 'white', highlightthickess = 1, command = self.message.destroy).pack(pady = 10)

class Invalid(): # To notify Invalid Input
    def __init__(self, root, invalid_type):
        # Setup tab
        self.root = root
        self.invalid_type = invalid_type
        self.invalid = Toplevel(root)
        self.invalid.title(" ")
        self.invalid.geometry("400x200")
        self.invalid.resizable(False, False)
        self.invalid.config(bg = 'white')

        # Dynamic Tile and Message
        title_map = {'account': ("Invalid Account", "Please double-check your email or password"),
                     'quantities': ("Invalid Quantities", "Please input No. of books borrow lower than Availible quantities and larger than zero.")}
        
        # Title Label
        Label(self.invalid, text = title_map[invalid_type][0], font = ('Arial', 18, 'bold'), bg = 'white', fg = 'black').pack(pady = (20,10))
        # Message Label
        Label(self.invalid, text = title_map[invalid_type][1], font = ('Arial', 12), bg = 'white', fg = 'black').pack(pady = (10,10))


class Sign_Out(): # To Sign Out
    def __init__(self, root):
        # Setup tab
        self.root = root
        self.sign_out = Toplevel(root)
        self.sign_out.title(" ")
        self.sign_out.geometry("400x200")
        self.sign_out.resizable(False, False)
        self.sign_out.config(bg = 'white')

        # Tiltle Label
        Label(self.sign_out, text = "Sign Out", font = ('Arial', 18, 'bold'), bg = 'white', fg = 'black').pack(pady = (20,10))
        # Message Label
        Label(self.sign_out, text = "Are you sure you want to sign out?", font = ('Arial', 12), bg = 'white', fg = 'black').pack(pady = (10,10))

        # Yes button
        Button(self.sign_out, width = 13, text = 'Yes', highlightbackground = 'white', highlightthickess = 1, command = self.sign_out.destroy).pack(pady = 10) # Thế command = function switch_to_log_in
        # No button
        Button(self.sign_out, width = 13, text = 'No', highlightbackground = 'white', highlightthickess = 1, command = self.sign_out.destroy).pack(pady = 10)

        # def switch_to_log_in(): # When clicked "Yes" button, the main window will switch to Log In window

class Print_Receipt():
    def __init__(self, root, receipt):
        # Setup tab
        self.root = root
        self.print_receipt = Toplevel(root)
        self.print_receipt.title(" ")
        self.print_receipt.geometry("300x150")
        self.print_receipt.resizable(False, False)
        self.print_receipt.config(bg = 'white')
        
        #Title Label
        Label(self.print_receipt, text = "Added Successfully!", font = ('Arial', 18, 'bold'), bg = 'white', fg = 'black').pack(pady = (20,10))

        # OK button
        Button(self.print_receipt, width = 13, text = 'Print Receipt?', highlightbackground = 'white', highlightthickess = 1, command = self.print_receipt.destroy).pack(pady = 10) # Thế command = function display_receipt

        # def display_receipt(): # When clicked "Print Receipt" button, new receipt generate, switch to Receipt window

class Drop_Off(): # To notify Book drop off successfully
    def __init__(self, root): # thêm receipt_id vào ()
        # Setup tab
        self.root = root
        self.drop_off = Toplevel(root)
        self.drop_off.title(" ")
        self.drop_off.geometry("350x150")
        self.drop_off.resizable(False, False)
        self.drop_off.config(bg = 'white')

        # Fetch receipt status
        # self.receipt = Receipt()
        # self.status = self.receipt.get_status_by_receipt_id(self.receipt_id)

        # Title Label
        Label(self.drop_off, text = "Drop Off Successfully!", font = ('Arial', 18, 'bold'), bg = 'white', fg = 'black').pack(pady = (20,10))

        # Ok button
        Button(self.drop_off, width = 13, text = 'OK', highlightbackground = 'white', highlightthickess = 1, command = self.handle_ok).pack(pady = 10)

        def handle_ok(self):
            self.drop_off.destroy()
            # if self.status == 'Overdue':
                # self.root.switch_to_overdue()
            # else:
                # self.root.switch_to_borrow/return()

class Pay_Fine(): # To notify Fine Paid
    def __init__(self, root):
        # Setup tab
        self.root = root
        self.pay_fine = Toplevel(root)
        self.pay_fine.title(" ")
        self.pay_fine.geometry("350x150")
        self.pay_fine.resizable(False, False)
        self.pay_fine.config(bg = 'white')

        # Title Label
        Label(self.pay_fine, text = "Drop Off Successfully!", font = ('Arial', 18, 'bold'), bg = 'white', fg = 'black').pack(pady = (20,10))

        # Ok button
        Button(self.pay_fine, width = 13, text = 'OK', highlightbackground = 'white', highlightthickess = 1, command = self.handle_ok).pack(pady = 10)

        def handle_ok(self):
            self.pay_fine.destroy()
            # self.root.switch_to_borrow/return()