from Model.admin_model import Admin
from View.noti_tab_view_1 import Delete, Message_1
from tkinter import messagebox
import sqlite3
class Delete_Users:
    def __init__(self, root=None):
        """Initialize the UserController"""
        self.root = root
        self.admin = Admin()  # Create an admin instance for user management operations
        self.selected_user = None  # Store the currently selected user


    def set_selected_user(self, user_data):
        """Set the currently selected user"""
        self.selected_user = user_data
        return True


    def delete_user_account(self):
        """Delete the selected user account"""
        if not self.selected_user or not self.selected_user.get('user_id'):
            return False
       
        # Show confirmation message box
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user account?")
        if confirm:
            return self.confirm_delete_user()
       
        return False


    def confirm_delete_user(self):
        """Confirm and execute user deletion"""
        if not self.selected_user or not self.selected_user.get('user_id'):
            return False
       
        # Perform deletion using Admin model
        result = self.admin.delete_user(self.selected_user['user_id'])
       
        # Show success message
        if result:
            Message_1(self.root, 'account')
            return True
        return False

    def delete_user_from_db(self, user_id):
        """Xóa người dùng khỏi database"""
        try:
            conn = sqlite3.connect("Library.db")  # Đảm bảo đúng đường dẫn file database
            cursor = conn.cursor()


            # Kiểm tra xem user có tồn tại hay không
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (int(user_id),))
            user_exists = cursor.fetchone()


            if not user_exists:
                print(f"User ID {user_id} not found in database.")
                conn.close()
                return False


            # Thực hiện xóa user
            cursor.execute("DELETE FROM users WHERE user_id = ?", (int(user_id),))
            conn.commit()
            conn.close()
            print(f"Successfully deleted user ID {user_id}")
            return True


        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        except Exception as e:
            print(f"Exception in delete_user_from_db: {e}")
            return False