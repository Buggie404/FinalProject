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
    def __init__(self, user_id=None):
        """
        Initialize the controller for editing account information
        
        Parameters:
        user_id (int): The ID of the user being edited
        """
        self.user_id = user_id
        self.current_user = None
        
        # If user_id is provided, load the user
        if user_id:
            user_data = User.get_id(user_id)
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
        bool: True if valid, False otherwise
        """
        # Check if username is empty
        if not username or username.strip() == "":
            return (False, "Username cannot be empty!", False)
            
        # Check if username is the same as current (no change)
        if self.current_user and self.current_user.username == username:
            return (True, "", False)
            
        # Check for new_username format
        if len(username) > 15:
            return (False, "Username must be maximum 15 characters!", False)
        
        if " " in username:
            return (False, "Username must not contain space", False)
        
        valids_chars_pattern = re.compile(r'^[a-zA-Z0-9\W_]+$')
        if not valids_chars_pattern.match(username):
            return (False, "Invalid username format", False)
        
        # Check if username is already taken
        existing_user = User.get_username(username)
        if existing_user:
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
        
        # Try YYYY-MM-DD format (the desired format)
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            try:
                date_of_birth = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                pass
        
        # Try MM/DD/YYYY format (what the user might enter)
        if date_of_birth is None and re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', date_str):
            try:
                date_of_birth = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
                return (False, "Please use YYYY-MM-DD format (e.g., 2010-06-03 instead of 06/03/2010).")
            except ValueError:
                pass
        
        # If we couldn't parse the date in any recognized format
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
        """
        Handler for the Apply button click in the edit info view
        
        Parameters:
        app (AccountEditInfoApp): The current view instance
        """
        # Get values from entry fields
        new_username = app.entries["lnE_NewUsername"].get()
        new_date_of_birth = app.entries["lnE_NewDateOfBirth"].get()
        
        # First check for format errors before checking if username is taken
        
        # Validate username format first (without checking if taken)
        username_valid, username_error, username_taken = self.validate_username(new_username)
        
        # If there's a format error with username (not related to it being taken)
        if not username_valid and not username_taken:
            messagebox.showerror("Invalid Username", username_error)
            return
        
        # Validate date of birth format
        dob_valid, dob_error = self.validate_date_of_birth(new_date_of_birth)
        if not dob_valid:
            messagebox.showerror("Invalid Date of Birth", dob_error)
            return
        
        # At this point, all format validations have passed
        # Now we check if the username is taken (which would redirect to AccountEditInfo2)
        if username_taken:
            # Close current window
            app.root.destroy()
            # Show the failure view for taken username
            self.show_failure_view()
            return
        
        # Process the edit request - at this point both validations have passed
        # and username is not taken
        result = self.current_user.edit_account_info(new_username, new_date_of_birth)
        
        # Close current window
        app.root.destroy()
        
        # Open success view since validation passed
        if result:
            self.show_success_view()
        else:
            # This should only occur if there's a database error or other issue
            messagebox.showerror("Error", "An unexpected error occurred while updating your information.")
    
    def show_success_view(self):
        """Display the success view"""
        from View.AccountManagement.AccountEditInfo1 import AccountEditInfo1
        root = Tk()
        app = AccountEditInfo1(root, user_id=self.user_id)
        app.run()
    
    def show_failure_view(self):
        """Display the failure view"""
        from View.AccountManagement.AccountEditInfo2 import AccountEditInfo2App
        root = Tk()
        app = AccountEditInfo2App(root)
        app.run()

# Function to initialize the controller with a user ID
def edit_account_info(user_id):
    """
    Initialize and start the account edit info workflow
    
    Parameters:
    user_id (int): The ID of the user to edit
    """
    controller = AccountEditInfoController(user_id)
    controller.start_edit_view()

# For testing purposes
if __name__ == "__main__":
    controller = AccountEditInfoController()
    controller.start_edit_view()