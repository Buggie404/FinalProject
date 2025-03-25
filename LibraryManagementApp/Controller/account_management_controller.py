"""To handle Edit Password and Information"""
# Import required libraries
import os
import sys
import datetime
from tkinter import Tk, messagebox
import re

# Set up path to access Model and View
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, "Model"))
sys.path.append(os.path.join(base_dir, "View"))
sys.path.append(os.path.join(base_dir, "View", "AccountManagement"))

# Import model and views
from Model.user_model import User

class AccountEditInfoController: # For Edit Account Information
    def __init__(self, user_data=None):
        """
        Initialize the controller for editing account information
        
        Parameters:
        user_id (int): The ID of the user being edited
        """
        self.user_data = user_data
        self.current_user = None

        if user_data:
            self.current_user = User(
                user_id=user_data[0],
                name=user_data[1],
                username=user_data[2],
                email=user_data[3],
                password=user_data[4],
                date_of_birth=user_data[5],
                role=user_data[6]
            )
    
    def validate_username(self, username):
        """
        Validate if the username is in an acceptable format and not already taken

        Parameters:
            username (str): The username to validate

        Returns:
            tuple: (is_valid, error_message, is_username_taken)
        """
        # Check if username is empty
        if not username or username.strip() == "":
            return (False, "Username cannot be empty!", False)

        # Check if username is the same as current (no change)
        if self.current_user and self.current_user.username == username:
            return (True, "", False)  # Valid, no error, not taken by someone else

        # Check for new_username format
        if len(username) > 15:
            return (False, "Username must be maximum 15 characters!", False)

        if " " in username:
            return (False, "Username must not contain space", False)

        valids_chars_pattern = re.compile(r'^[a-zA-Z0-9\W_]+$')
        if not valids_chars_pattern.match(username):
            return (False, "Invalid username format", False)

        # Check if username is already taken by another user
        existing_user = User.get_username(username)
        if existing_user:
            # Check if the existing user is not the current user
            if existing_user[0] != self.user_data:
                return (False, "Username is already taken", True)

        return (True, "", False)
    
    def validate_date_of_birth(self, date_str):
        """
        Validate if the date is in an acceptable format, not in the future,
        and at least 10 years ago
        
        Parameters:
        date_str (str): The date string to validate
        
        Returns:
        tuple: (is_valid, error_message)
        """
        # Check if date is empty
        if not date_str or date_str.strip() == "":
            return (False, "Date of birth cannot be empty.")
        
        # Try to parse different date formats
        date_of_birth = None
        
        # Try YYYY-MM-DD format
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            try:
                date_of_birth = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                pass
        
        # Try MM/DD/YYYY format
        if date_of_birth is None and re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', date_str):
            try:
                date_of_birth = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
                return (False, "Please use YYYY-MM-DD format (e.g., 2010-06-03 instead of 06/03/2010).")
            except ValueError:
                pass
        
        if date_of_birth is None:
            return (False, "Invalid date format. Please use YYYY-MM-DD format.")
        
        # Get current date
        current_date = datetime.datetime.now().date()
        
        # Check if date is in the future
        if date_of_birth > current_date:
            return (False, "Date of birth cannot be in the future.")
        
        # Calculate minimum allowed date (10 years ago)
        min_date = current_date.replace(year=current_date.year - 10)
        
        # Check if date is at least 10 years ago
        if date_of_birth > min_date:
            return (False, "You must be at least 10 years old to register.")
        
        return (True, "")
    
    def process_edit_request(self, new_username, new_date_of_birth):
        """
        Process the edit request with validation
        
        Parameters:
        new_username (str): The new username to set
        new_date_of_birth (str): The new date of birth to set
        
        Returns:
        bool: True if edit was successful, False otherwise
        """
        # Check if user is loaded
        if not self.current_user:
            return False
                
        # Validate inputs
        username_valid, _, username_taken = self.validate_username(new_username)
        if not username_valid:
            return False
                
        dob_valid, _ = self.validate_date_of_birth(new_date_of_birth)
        if not dob_valid:
            return False
                
        # Call model to update information
        result = self.current_user.edit_account_info(new_username, new_date_of_birth)
        return result
    
    def start_edit_view(self):
        """Launch the edit account information view"""
        from View.AccountManagement.AccountEditInfo import AccountEditInfoApp
        root = Tk()
        app = AccountEditInfoApp(root)
        
        # Set the apply button command
        app.buttons["btn_Apply"].config(
            command=lambda: self.handle_apply_click(app)
        )
        
        # If user is loaded, prefill fields with current values
        if self.current_user:
            if app.entries.get("lnE_NewUsername") and self.current_user.username:
                app.entries["lnE_NewUsername"].insert(0, self.current_user.username)
                
            if app.entries.get("lnE_NewDateOfBirth") and self.current_user.date_of_birth:
                app.entries["lnE_NewDateOfBirth"].insert(0, self.current_user.date_of_birth)
                
        app.run()
    
    def handle_apply_click(self, app):
        """Handler for the Apply button click in the edit info view
        
        Parameters:
            app (AccountEditInfoApp): The current view instance
        """
        # Get values from entry fields
        new_username = app.entries["lnE_NewUsername"].get()
        new_date_of_birth = app.entries["lnE_NewDateOfBirth"].get()
        
        # Get current username for comparison
        current_username = self.current_user.username if self.current_user else None
        
        # Check if username is unchanged
        if current_username and new_username == current_username:
            # Skip username validation if unchanged
            username_valid = True
            username_error = ""
            username_taken = False
        else:
            # Validate username format and check if taken
            username_valid, username_error, username_taken = self.validate_username(new_username)
        
        # If there's a format error with username
        if not username_valid and not username_taken:
            messagebox.showerror("Invalid Username", username_error)
            return
        
        # Validate date of birth format
        dob_valid, dob_error = self.validate_date_of_birth(new_date_of_birth)
        if not dob_valid:
            messagebox.showerror("Invalid Date of Birth", dob_error)
            return
        
        if username_taken:
            # Close current window
            app.root.destroy()
            # Show the failure view for taken username
            self.show_failure_view()
            return
        
        result = self.current_user.edit_account_info(new_username, new_date_of_birth)
        
        # Close current window
        app.root.destroy()
        
        # Open success view since validation passed
        if result:
            self.show_success_view()
        else:
            messagebox.showerror("Error", "An unexpected error occurred while updating your information.")

    def show_success_view(self):
        """Display the success view"""
        from View.AccountManagement.AccountEditInfo1 import AccountEditInfo1
        root = Tk()
        app = AccountEditInfo1(root, user_data=self.user_data)
        app.run()
    
    def show_failure_view(self):
        """Display the failure view"""
        from View.AccountManagement.AccountEditInfo2 import AccountEditInfo2App
        root = Tk()
        app = AccountEditInfo2App(root, user_data=self.user_data)
        app.run()

# Function to initialize the controller with a user ID
def edit_account_info(user_data):
    """
    Initialize and start the account edit info workflow
    
    Parameters:
    user_id (int): The ID of the user to edit
    """
    controller = AccountEditInfoController(user_data)
    controller.start_edit_view()

class PasswordChangeController:
    def __init__(self, user_data=None):
        """Initialize controller with user data"""
        self.user_data = user_data
        self.current_user = None

        # If user_data is provided, create User object
        if user_data:
            self.current_user = User(
                user_id=user_data[0],
                name=user_data[1],
                username=user_data[2],
                email=user_data[3],
                password=user_data[4],
                date_of_birth=user_data[5],
                role=user_data[6]
            )
        
        # Track validation errors
        self.validation_errors = {
            'current_password': False,
            'new_password': False,
            'confirm_password': False
        }

    def validate_current_password(self, current_password):
        """Validate that current password matches the user's actual password"""
        if not current_password:
            return False, "Current password cannot be empty."

        if self.user_data and current_password != self.user_data[4]:
            self.validation_errors['current_password'] = True
            return False, "Current password is incorrect."

        self.validation_errors['current_password'] = False
        return True, ""

    def validate_new_password(self, new_password):
        """Validate new password requirements"""
        if not new_password:
            return False, "New password cannot be empty."

        # Check length (8-15 characters)
        if len(new_password) < 8:
            self.validation_errors['new_password'] = True
            return False, "Password must be at least 8 characters."

        if len(new_password) > 15:
            self.validation_errors['new_password'] = True
            return False, "Password must be less than 15 characters."

        # Check for spaces
        if ' ' in new_password:
            self.validation_errors['new_password'] = True
            return False, "Password cannot contain spaces."

        # Check for valid characters
        valid_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*_-+=`|\\(){}[]:;'<>,. ?/"
        for char in new_password:
            if char not in valid_chars:
                self.validation_errors['new_password'] = True
                return False, f"Password contains invalid character: {char}"

        self.validation_errors['new_password'] = False
        return True, ""

    def validate_confirm_password(self, new_password, confirm_password):
        """Validate that confirm password matches new password"""
        if not confirm_password:
            return False, "Confirm password cannot be empty."

        if new_password != confirm_password:
            self.validation_errors['confirm_password'] = True
            return False, "Passwords do not match."

        self.validation_errors['confirm_password'] = False
        return True, ""
    
    def validate_current_password_field(self, current_password):
        """Validate current password field - for FocusOut event
        Returns: (is_valid, error_message, should_show_error)
        """
        # Skip validation if empty (will be caught when submitting)
        if not current_password:
            return True, "", False
            
        valid, message = self.validate_current_password(current_password)
        return valid, message, not valid
    
    def validate_new_password_field(self, new_password):
        """Validate new password field - for FocusOut event
        Returns: (is_valid, error_message, should_show_error)
        """
        # Skip validation if empty (will be caught when submitting)
        if not new_password:
            return True, "", False
            
        valid, message = self.validate_new_password(new_password)
        return valid, message, not valid
    
    def validate_confirm_password_field(self, new_password, confirm_password):
        """Validate confirm password field - for FocusOut event
        Returns: (is_valid, error_message, should_show_error)
        """
        # Skip validation if empty (will be caught when submitting)
        if not confirm_password:
            return True, "", False
            
        valid, message = self.validate_confirm_password(new_password, confirm_password)
        return valid, message, not valid
    
    def process_password_change(self, current_password, new_password, confirm_password):
        """Process password change with all validations
        
        Returns:
            tuple: (success, message, redirect_to_success, field_to_focus)
        """
        # Check for empty fields first
        if not current_password:
            return False, "Current password cannot be empty.", False, "current_password"
            
        if not new_password:
            return False, "New password cannot be empty.", False, "new_password"
            
        if not confirm_password:
            return False, "Confirm password cannot be empty.", False, "confirm_password"
        
        # Validate current password
        current_valid, current_msg = self.validate_current_password(current_password)
        if not current_valid:
            return False, current_msg, False, "current_password"
            
        # Validate new password format
        new_valid, new_msg = self.validate_new_password(new_password)
        if not new_valid:
            return False, new_msg, False, "new_password"
            
        # Check if passwords match
        match_valid, match_msg = self.validate_confirm_password(new_password, confirm_password)
        if not match_valid:
            return False, match_msg, True, "confirm_password"
        
        # All validations passed, update password
        try:
            # Update password in database
            if self.current_user:
                success = self.change_password(new_password)
                if success:
                    return True, "Password changed successfully!", True, None
                else:
                    return False, "Failed to update password in database.", True, None
            else:
                return False, "User not found.", True, None
        except Exception as e:
            print(f"Error changing password: {e}")
            return False, f"Error: {str(e)}", True, None

    def change_password(self, new_password):
        """Update the user's password in the database"""
        if not self.current_user:
            return False

        try:
            self.current_user.change_pass(new_password)
            
            # Update user_data with new password
            if self.user_data:
                self.user_data = list(self.user_data)
                self.user_data[4] = new_password
                self.user_data = tuple(self.user_data)
                
            return True
            
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
            
    def get_user_data(self):
        """Get the current user data"""
        return self.user_data
        
    def handle_navigation(self, button_name, view):
        """Handle navigation logic based on button clicks
        
        Args:
            button_name: The name of the button clicked
            view: The current view for accessing root
            
        Returns:
            bool: True if navigation handled, False otherwise
        """
        if button_name == "btn_ChangePassword":
            # When clicked Change Password on Change Password window -> go back to Account MainWindow
            view.root.destroy()
            from View.AccountManagement.AccountMan import AccountManagement
            accountman_root = Tk()
            accountman = AccountManagement(accountman_root, user_data=self.user_data)
            accountman_root.mainloop()
            return True
            
        elif button_name == "btn_EditAccountInformation":
            view.root.destroy()
            from View.AccountManagement.AccountEditInfo import AccountEditInfoApp
            editinfo_root = Tk()
            editinfo = AccountEditInfoApp(editinfo_root, user_data=self.user_data)
            editinfo_root.mainloop()
            return True
            
        elif button_name == "btn_BackToHomepage":
            view.root.destroy()
            from View.Homepage import HomepageApp
            role = 'admin' if self.user_data[6] == 'Admin' else 'User'
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role=role,  user_data=self.user_data)
            homepage_root.mainloop()
            return True
            
        return False