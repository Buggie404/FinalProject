from Model.user_model import User
from Model.admin_model import Admin
from View.noti_tab_view_1 import Message_1, Message_2, Invalid
from tkinter import messagebox

class ResetPasswordController:
    """
    Controller class to handle password reset functionality for admin users.
    Connects UserEditAccount and UserEditAccount1 views with User and Admin models.
    """
    # Define default password as a class constant for easy reference
    DEFAULT_PASSWORD = "123456789"
    
    def __init__(self):
        """Initialize the controller with an Admin model instance"""
        self.admin = Admin()
        
    def validate_user_id(self, user_id):
        """
        Validate if a user exists with the given user_id
        
        Args:
            user_id (str): The user ID to validate
            
        Returns:
            tuple or None: User data if found, None otherwise
        """
        # Check if user_id is empty
        if not user_id or user_id.strip() == "":
            return None
            
        try:
            # Convert to integer if possible (handle both string and int inputs)
            if user_id.isdigit():
                user_id = int(user_id)
                
            # Get user data from the model
            user_data = User.get_id(user_id)
            return user_data
            
        except Exception as e:
            print(f"Error validating user ID: {e}")
            return None
    
    def is_password_already_default(self, user_data):
        """
        Check if the user's password is already the default password
        
        Args:
            user_data (tuple): User data tuple from database
            
        Returns:
            bool: True if password is already default, False otherwise
        """
        # Password is typically at index 4 in the user_data tuple
        return user_data and user_data[4] == self.DEFAULT_PASSWORD
    
    def reset_user_password(self, user_id, root_window):
        """
        Reset the password for the specified user to the default password
        
        Args:
            user_id: The ID of the user whose password will be reset
            root_window: The root window for displaying notifications
            
        Returns:
            bool: True if password reset was successful, False otherwise
        """
        try:
            # Get current user data to check current password
            user_data = User.get_id(user_id)
            
            if not user_data:
                Message_1(root_window, 'edit_pass_id')
                return False
                
            # Check if password is already the default
            if self.is_password_already_default(user_data):
                messagebox.showinfo(
                    "Password Already Default", 
                    f"The user's password is already set to the default password."
                )
                return False
                
            # Attempt to reset the password using Admin model
            success = self.admin.reset_password(user_id)
            
            if success:
                # Display success message
                Message_2(root_window, 'pass_reset')
                return True
            else:
                # Display error message
                Message_1(root_window, 'edit_pass_id')
                return False
                
        except Exception as e:
            print(f"Error resetting password: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return False
    
    def get_user_details(self, user_id):
        """
        Get detailed user information for display in the second window
        
        Args:
            user_id: The ID of the user to retrieve details for
            
        Returns:
            dict: User details in a format suitable for display
        """
        user_data = self.validate_user_id(user_id)
        
        if user_data:
            # Based on the user_model.py file structure, user_data would be a tuple
            # with fields in the order defined in the __init__ method of User class
            return {
                'user_id': user_data[0],
                'name': user_data[1],
                'username': user_data[2],
                'email': user_data[3],
                'password': user_data[4],  # Note: We don't display this, just included for completeness
                'date_of_birth': user_data[5],
                'role': user_data[6]
            }
        return None
    
    def validate_input(self, user_id, root_window):
        """
        Validate the user input ID
        
        Args:
            user_id (str): The user ID to validate
            root_window: The root window for displaying notifications
            
        Returns:
            bool: True if input is valid, False otherwise
        """
        # Check if user_id is empty
        if not user_id or user_id.strip() == "":
            Invalid(root_window, 'Input')
            return False
            
        # Check if user exists
        user_data = self.validate_user_id(user_id)
        if not user_data:
            Message_1(root_window, 'edit_pass_id')
            return False
            
        return True
    
    def switch_to_user_edit_account1(self, root_window, user_id):
        """
        Switch from UserEditAccount to UserEditAccount1 with user data
        
        Args:
            root_window: The current root window
            user_id: The ID of the user to display
            
        Returns:
            bool: True if switch was successful, False otherwise
        """
        # Validate input first
        if not self.validate_input(user_id, root_window):
            return False
            
        try:
            from tkinter import Tk
            from View.UserManagement.UserEditAccount1 import UserEditAccountApp as UserEditAccount1App
            
            # Get user details
            user_data = self.get_user_details(user_id)
            
            if user_data:
                # Close current window
                root_window.destroy()
                
                # Create new window with user data
                reset_1_root = Tk()
                reset_1 = UserEditAccount1App(reset_1_root)
                
                # Update the labels with user data
                # We need to wait for the canvas to be created
                reset_1_root.update()
                
                # Now update the text of the labels
                reset_1.canvas.itemconfig(reset_1.lbl_ID, text=str(user_data['user_id']))
                reset_1.canvas.itemconfig(reset_1.lbl_Name, text=user_data['name'])
                reset_1.canvas.itemconfig(reset_1.lbl_EmailAddress, text=user_data['email'])
                reset_1.canvas.itemconfig(reset_1.lbl_Username, text=user_data['username'])
                
                # Store the user_id for later use when resetting password
                reset_1.current_user_id = user_data['user_id']
                
                # Add command to reset password button
                reset_1.buttons["btn_ResetPassword"].config(
                    command=lambda: self.reset_user_password(reset_1.current_user_id, reset_1_root)
                )
                
                reset_1_root.mainloop()
                return True
                
        except Exception as e:
            print(f"Error switching to UserEditAccount1: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return False
