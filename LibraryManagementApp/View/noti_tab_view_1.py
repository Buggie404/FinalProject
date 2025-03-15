# Import Lib
from tkinter import *
from LogIn import LoginApplication


# Import First_Sub_Win and Current_sub_Win
# from first-sub-win import frst-sub class
# from current-sub-win import current-sub class

class Delete():  # To confirm delection
    def __init__(self, root, delete_type):
        """delete_type: 'book' or 'account"""

        # Config Notification tab
        self.root = root
        self.delete_type = delete_type
        self.delete_noti = Toplevel(root)

        # Dynamic Title and Messages
        delete_map = {'book': ('Delete Book', "Are you sure you wnat to delete this book?"),
                      'account': ('Delete Account', "Are you sure you wnat to delete this account?")}

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
        Button(self.delete_noti, width=13, text="Yes", highlightbackground='white', highlighthickness=1,
               command=lambda: self.choice('yes')).pack(pady=10)
        # No Button
        Button(self.delete_noti, width=13, text="No", highlightbackground='white', highlightthickness=1,
               command=lambda: self.choice('no')).pack(pady=10)

    # Choice function
    def choice(self, option):
        if option == 'yes':  # When clicked 'Yes' button -> switch to notify mess
            # Cho chức năng xoá sách từ Controller vào
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

        # Dynamic Message
        message_1_map = {'book': "Book Deleted!",
                         'account': "Account Deleted!",
                         'edit_pass_id': 'No match ID!',
                         'edit_book_id': "No match ISBN!",
                         'receipt': "No match receipt ID!"}

        # Tile Label
        Label(self.message_1, text=message_1_map[delete_type], font=("Montserrat", 18, 'bold'), bg='white',
              fg='black').pack(pady=(20, 10))

        # OK Button
        Button(self.message_1, width=13, text="OK", highlightbackground='white', highlightthickess=1,
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
        Button(self.message_2, width=13, text="Return", highlightbackground='white', highlightthickess=1,
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


class Invalid():  # To notify Invalid input
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
                                    "No. of books borrow need to be larger than zero and lower or equal to Availible quantities")}

        # Title Label
        Label(self.invalid, text=invalid_map[invalid_type][0], font=("Montserrat", 18, 'bold'), bg='white',
              fg='black').pack(pady=(20, 10))
        # Message Label
        Label(self.invalid, text=invalid_map[invalid_type][1], font=("Montserrat", 12), bg='white', fg='black').pack(
            pady=(10, 10))

        # Ok button
        Button(self.invalid, width=13, text="OK", highlightbackground='white', highlightthickess=1,
               command=lambda: self.invalid.destroy).pack(pady=10)


class Drop_Off():
    def __init__(self, root, receipt_status):
        # Config Notification tab
        self.root = root
        self.delete_noti = Toplevel(root)
        self.delete_noti.title(" ")
        self.delete_noti.geometry("400x200")
        self.delete_noti.resizable(False, False)
        self.delete_noti.config(bg='white')
        self.status = receipt_status

        # Title Label
        Label(self.delete_noti, text="Drop Off Successfully!", font=('Montserrat', 18, 'bold'), bg='white',
              fg='black').pack(pady=(20, 10))

        # Config to switch window depands on receipt_status
        # if receipt_status == 'overdue': -> switch to overdue window, else: -> switch back to first-window


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
        self.sign_out.destroy()  # Close the Sign_Out window
        self.root.destroy()  # Close the main root

        # Create a new root for LogIn
        log_in_root = Tk()
        LoginApplication(log_in_root)  # Assuming you have a LogIn class
        log_in_root.mainloop()


class Print_Receipt():  # To print out receipt, when clicked 'Print Receipt?' -> switch to Print_Receipt window
    pass