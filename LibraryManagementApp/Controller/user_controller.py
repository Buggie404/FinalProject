""" To handle any function related to user management """
# Import fetched data from Admin Model
from Model.admin_model import Admin
from Model.user_model import User
from tkinter import messagebox
from View.noti_tab_view_1 import Delete, Message_1
import sqlite3
import re
import datetime
import unidecode
import os
import sys

# Add parent directory to path to import from Model
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Model.user_model import User

class Search_users: # Handel search function
    def __init__(self):
        pass

    @staticmethod
    def search_by_id(user_id):
        if not user_id:
            return False, "There are no matching IDs!"

        user = User.get_id(user_id)
        if user:
            return True, user
        return False, "There are no matching IDs!"

    @staticmethod
    def search_by_username(username):
        if not username:
            return False, "There are no matching usernames!"

        user = User.get_username(username)
        if user:
            return True, user
        return False, "There are no matching usernames!"
        
    @staticmethod
    def filter_users_by_id(search_term):
        """
        Filter users by exact ID match
        
        Args:
            search_term (str): The user ID to search for
            
        Returns:
            tuple: (success_flag, result)
                - If successful and user found: (True, user_data)
                - If successful but no user found: (False, "no_match_id")
                - If search_term is empty: (False, "empty_search")
        """
        if not search_term or search_term.strip() == "" or search_term == "Search":
            return False, "empty_search"
            
        try:
            # Convert to integer if possible (assuming IDs are integers)
            user_id = int(search_term)
            user = User.get_id(user_id)
            
            if user:
                return True, user
            else:
                return False, "no_match_id"
                
        except ValueError:
            # If search term cannot be converted to integer
            return False, "invalid_id_format"
    
    @staticmethod
    def filter_by_user_id(tbl_User, search_term, load_user_func):
        """
        Filter the user table by user_id
        
        Args:
            tbl_User: The Treeview widget containing user data
            search_term (str): The search term to filter by
            load_user_func: Function to reload all users
            
        Returns:
            None
        """
        # Skip filtering if the search term is the placeholder or empty
        if search_term == "Search" or search_term.strip() == "":
            # Reload all users
            load_user_func()
            return
        
        print(f"Filtering by user_id: {search_term}")
        
        try:
            # Use the filter_users_by_id method
            success, result = Search_users.filter_users_by_id(search_term)
            
            if success:
                # Clear existing data
                for item in tbl_User.get_children():
                    tbl_User.delete(item)
                
                # Display the single user found
                user = result
                tbl_User.insert('', 'end', values=(
                    user[0],  # User_id
                    user[1],  # name
                    user[2],  # username
                    user[3],  # email
                    user[5],  # date_of_birth
                    user[6]   # role
                ))
            else:
                # Show error message
                messagebox.showinfo("Search Result", result)
                # Reload all users if no match found
                load_user_func()
                
        except Exception as e:
            print(f"Error filtering users: {e}")
            # Reload all users if filtering fails
            load_user_func()
    
    @staticmethod
    def original_filter_by_user_id(tbl_User, search_term, load_user_func):
        """
        Original filter method for partial matches
        
        Args:
            tbl_User: The Treeview widget containing user data
            search_term (str): The search term to filter by
            load_user_func: Function to reload all users
            
        Returns:
            None
        """
        try:
            # Clear the current view and reload all data
            load_user_func()
            
            # Get all items after reloading
            all_items = tbl_User.get_children()
            
            # First, hide all rows
            for item in all_items:
                tbl_User.detach(item)
            
            # Then, show only the matching rows
            for item in all_items:
                values = tbl_User.item(item, 'values')
                user_id = str(values[0])  # The first column is user_id
                
                if search_term.lower() in user_id.lower():
                    # Reattach the item to show it
                    tbl_User.reattach(item, '', 'end')
            
        except Exception as e:
            print(f"Error in original filtering method: {e}")
            # Reload all users if filtering fails
            load_user_func()

    @staticmethod
    def filter_users_by_username(search_term):
        """
        Filter users by exact username match
        
        Args:
            search_term (str): The username to search for
            
        Returns:
            tuple: (success_flag, result)
                - If successful and user found: (True, user_data)
                - If successful but no user found: (False, "no_match_username")
                - If search_term is empty: (False, "empty_search")
        """
        if not search_term or search_term.strip() == "" or search_term == "Search":
            return False, "empty_search"
            
        # No need to convert to integer as username can be alphanumeric
        user = User.get_username(search_term)
        
        if user:
            return True, user
        else:
            return False, "no_match_username"
        
    @staticmethod
    def filter_by_username(tbl_User, search_term, load_user_func):
        """
        Filter the user table by username
        
        Args:
            tbl_User: The Treeview widget containing user data
            search_term (str): The search term to filter by
            load_user_func: Function to reload all users
            
        Returns:
            None
        """
        # Skip filtering if the search term is the placeholder or empty
        if search_term == "Search" or search_term.strip() == "":
            # Reload all users
            load_user_func()
            return
        
        print(f"Filtering by username: {search_term}")
        
        try:
            # Use the filter_users_by_username method
            success, result = Search_users.filter_users_by_username(search_term)
            
            if success:
                # Clear existing data
                for item in tbl_User.get_children():
                    tbl_User.delete(item)
                
                # Display the single user found
                user = result
                tbl_User.insert('', 'end', values=(
                    user[0],  # User_id
                    user[1],  # name
                    user[2],  # username
                    user[3],  # email
                    user[5],  # date_of_birth
                    user[6]   # role
                ))
            else:
                # Try partial match instead
                success, result = Search_users.filter_users_by_partial_username(search_term)
                
                if success:
                    # Clear existing data
                    for item in tbl_User.get_children():
                        tbl_User.delete(item)
                    
                    # Display all matching users
                    for user in result:
                        tbl_User.insert('', 'end', values=(
                            user[0],  # User_id
                            user[1],  # name
                            user[2],  # username
                            user[3],  # email
                            user[5],  # date_of_birth
                            user[6]   # role
                        ))
                else:
                    # Show error message
                    messagebox.showinfo("Search Result", "No matching usernames found!")
                    # Reload all users if no match found
                    load_user_func()
                
        except Exception as e:
            print(f"Error filtering users: {e}")
            # Reload all users if filtering fails
            load_user_func()

    @staticmethod
    def filter_users(tbl_User, search_term, load_user_func, root = None):
        """
        Filter users by either user_id or username depending on the search term
        
        Args:
            tbl_User: The Treeview widget containing user data
            search_term (str): The search term to filter by
            load_user_func: Function to reload all users
            root: The root for creating notification
            
        Returns:
            None
        """
        # Skip filtering if the search term is the placeholder or empty
        if search_term == "Search" or search_term.strip() == "":
            # Reload all users
            load_user_func()
            return
        
        try:
            # Check if the search term is a number (likely an ID)
            is_id = search_term.isdigit()
            
            if is_id:
                print(f"Filtering by user_id: {search_term}")
                success, result = Search_users.filter_users_by_id(search_term)
                
                if success:
                    # Clear existing data
                    for item in tbl_User.get_children():
                        tbl_User.delete(item)
                    
                    # Display the single user found
                    user = result
                    tbl_User.insert('', 'end', values=(
                        user[0],  # User_id
                        user[1],  # name
                        user[2],  # username
                        user[3],  # email
                        user[5],  # date_of_birth
                        user[6]   # role
                    ))
                else:
                    from View.noti_tab_view_1 import Message_1
                    Message_1(root, "search_account")
                    load_user_func()
            else:
                print(f"Filtering by username: {search_term}")
                # Try exact match first
                success, result = Search_users.filter_users_by_username(search_term)
                
                if success:
                    # Clear existing data
                    for item in tbl_User.get_children():
                        tbl_User.delete(item)
                    
                    # Display the single user found
                    user = result
                    tbl_User.insert('', 'end', values=(
                        user[0],  # User_id
                        user[1],  # name
                        user[2],  # username
                        user[3],  # email
                        user[5],  # date_of_birth
                        user[6]   # role
                    ))
                else:
                    # Try partial match
                    success, result = Search_users.filter_users_by_partial_username(search_term)
                    
                    if success:
                        # Clear existing data
                        for item in tbl_User.get_children():
                            tbl_User.delete(item)
                        
                        # Display all matching users
                        for user in result:
                            tbl_User.insert('', 'end', values=(
                                user[0],  # User_id
                                user[1],  # name
                                user[2],  # username
                                user[3],  # email
                                user[5],  # date_of_birth
                                user[6]   # role
                            ))
                    else:
                        from View.noti_tab_view_1 import Message_1
                        Message_1(root, "search_account")
                        load_user_func()
                
        except Exception as e:
            print(f"Error filtering users: {e}")
            # Reload all users if filtering fails
            load_user_func()
    
    @staticmethod
    def filter_users_by_partial_username(search_term):
        """
        Filter users by partial username match
        
        Args:
            search_term (str): The partial username to search for
            
        Returns:
            tuple: (success_flag, result)
                - If successful and users found: (True, users_data)
                - If successful but no users found: (False, "no_match_username")
                - If search_term is empty: (False, "empty_search")
        """
        if not search_term or search_term.strip() == "" or search_term == "Search":
            return False, "empty_search"
            
        # Search for partial matches
        users = User.search_username_partial(search_term)
        
        if users and len(users) > 0:
            return True, users
        else:
            return False, "no_match_username"

class add_account:
    """Controller for handling user account creation operations"""
    
    # Class attribute instead of instance attribute
    default_password = "123456789"
    
    # Flag to track validation errors for each field
    field_validation_errors = {
        'name': False,
        'role': False,
        'date_of_birth': False
    }
    
    @staticmethod
    def process_user_form(name, role, date_of_birth):
        """
        Process user form data, validate it, and create a new user account
        
        Args:
            name (str): Full name of the user
            role (str): User role (either 'User' or 'Admin')
            date_of_birth (str): Date of birth in format YY/MM/DD
            
        Returns:
            tuple: (success_flag, message, user_data)
        """
        # Reset validation errors for a fresh form submission
        field_errors = {
            'name': False,
            'role': False,
            'date_of_birth': False
        }
        
        # Validate all fields at once and collect errors
        valid_name, name_msg = add_account.validate_name(name)
        if not valid_name:
            field_errors['name'] = True
            
        valid_role, role_msg, formatted_role = add_account.validate_role(role)
        if not valid_role:
            field_errors['role'] = True
            
        valid_date, date_msg = add_account.validate_date_format(date_of_birth)
        if not valid_date:
            field_errors['date_of_birth'] = True
        
        # If any field has an error, return without showing additional messages
        if any(field_errors.values()):
            # Update the class-level validation errors
            add_account.field_validation_errors = field_errors
            
            # Return only the first error message to avoid multiple warnings
            if not valid_name:
                return False, name_msg, {}
            elif not valid_role:
                return False, role_msg, {}
            elif not valid_date:
                return False, date_msg, {}
            
            return False, "Please correct the invalid fields and try again.", {}
        
        # Get next user ID
        user_id = add_account.get_next_user_id()
        
        # Generate username and email
        try:
            username, email = add_account.generate_username_and_email(name, user_id)
            if not username or not email:
                return False, "Could not generate username and email. Please check the name format.", {}
        except Exception as e:
            return False, f"Error generating username and email: {str(e)}", {}
        
        # Format date for database
        formatted_date = add_account.format_date_for_database(date_of_birth)
        
        # Create user data dictionary
        user_data = {
            'user_id': user_id,
            'name': name,
            'username': username,
            'email': email,
            'password': add_account.default_password,
            'date_of_birth': formatted_date,
            'role': formatted_role
        }
        
        # Create and save user directly without separate UserAccount class
        try:
            user = User(
                user_id=user_id, 
                name=name, 
                username=username, 
                email=email, 
                password=add_account.default_password, 
                date_of_birth=formatted_date, 
                role=formatted_role
            )
            
            # Add account attributes directly to the user object
            user.generated = True  # Flag to indicate auto-generated username/email
            
            # Save user with extended account properties
            success = user.save_user()
            
            # Reset validation errors after successful save
            add_account.field_validation_errors = {
                'name': False,
                'role': False,
                'date_of_birth': False
            }
            
            if not success:
                return False, "Failed to save user to database. The database might be locked.", {}
                
            return True, "User account created successfully!", user_data
        except Exception as e:
            return False, f"Error creating user: {str(e)}", {}
    
    @staticmethod
    def validate_name_on_event(name):
        """
        Validate name field when focus leaves the field
        
        Args:
            name (str): Name to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        valid, message = add_account.validate_name(name)
        add_account.field_validation_errors['name'] = not valid
        return valid, message
    
    @staticmethod
    def validate_role_on_event(role):
        """
        Validate role field when focus leaves the field
        
        Args:
            role (str): Role to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        valid, message, _ = add_account.validate_role(role)
        add_account.field_validation_errors['role'] = not valid
        return valid, message
    
    @staticmethod
    def validate_date_on_event(date_text):
        """
        Validate date field when focus leaves the field
        
        Args:
            date_text (str): Date to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        valid, message = add_account.validate_date_format(date_text)
        add_account.field_validation_errors['date_of_birth'] = not valid
        return valid, message
    
    @staticmethod
    def validate_name(name):
        """
        Validate that name contains only letters and spaces and is not empty
        
        Args:
            name (str): Name to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not name or name.strip() == "":
            return False, "Name cannot be empty."
        
        # Check for numbers or special characters
        if re.search(r'[^a-zA-ZÀ-ỹ\s]', name):
            return False, "Name should contain only letters and spaces."
        
        return True, ""
    
    @staticmethod
    def validate_role(role):
        """
        Validate that role is either 'User' or 'Admin' (case-sensitive)
        
        Args:
            role (str): Role to validate
            
        Returns:
            tuple: (is_valid, error_message, formatted_role)
        """
        if not role or role.strip() == "":
            return False, "Role cannot be empty.", ""
        
        # Case-sensitive comparison (no longer using lowercase)
        if role == "User":
            return True, "", "User"
        elif role == "Admin":
            return True, "", "Admin"
        else:
            return False, "Role must be exactly 'User' or 'Admin'.", ""
    
    @staticmethod
    def validate_date_format(date_text):
        """
        Validate date format (YYYY/MM/DD)
        
        Args:
            date_text (str): Date text to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not date_text or date_text.strip() == "":
            return False, "Date of birth cannot be empty."
        
        # Allow only numbers and / character
        if re.search(r'[^0-9/]', date_text):
            return False, "Date should contain only numbers and / character."
        
        try:
            # Check format
            if not re.match(r'^(\d{4})/(\d{2})/(\d{2})$', date_text):
                return False, "Invalid date format. Use YYYY/MM/DD."
            
            # Parse date
            year, month, day = date_text.split('/')
            
            # Convert to integers
            year_int = int(year)
            month_int = int(month)
            day_int = int(day)
            
            # Basic validation
            if not (1 <= month_int <= 12 and 1 <= day_int <= 31):
                return False, "Invalid month or day."
                
            # Create date object for additional validation
            date_obj = datetime.datetime(year_int, month_int, day_int)
            
            # Check if date is in the future
            if date_obj.date() > datetime.datetime.now().date():
                return False, "Date of birth cannot be in the future."
                
            return True, ""
            
        except ValueError:
            return False, "Invalid date. Please use YYYY/MM/DD format."
    
    # Rest of the existing methods remain unchanged
    @staticmethod
    def format_date_for_database(date_text):
        """
        Convert date from YY/MM/DD to YYYY-MM-DD for database
        
        Args:
            date_text (str): Date in YY/MM/DD format
            
        Returns:
            str: Date in YYYY-MM-DD format
        """
        if not date_text or date_text.strip() == "":
            return None
            
        try:
            date_parts = date_text.split('/')
            if len(date_parts) == 3:
                year, month, day = date_parts
                # Add century to year if needed
                if len(year) == 2:
                    current_year = datetime.datetime.now().year
                    century = str(current_year)[:2]
                    year = century + year
                return f"{year}-{month}-{day}"
            return None
        except Exception:
            return None
    
    @staticmethod
    def get_next_user_id():
        """
        Get the next available user ID from the database
        
        Returns:
            int: Next available user ID
        """
        try:
            users = User.get_all_user()
            if users:
                # Find the highest user_id
                max_id = max([int(user[0]) for user in users])
                return max_id + 1
            return 1  # Default if no users
        except Exception as e:
            print(f"Error getting next user ID: {str(e)}")
            return 167  # Default fallback value
    
    @staticmethod
    def generate_username_and_email(name, user_id):
        """
        Generate username and email based on full name and user ID
        
        Args:
            name (str): Full name of the user
            user_id (int): User ID
            
        Returns:
            tuple: (username, email)
        """
        if not name or len(name.split()) < 2:
            return None, None
        
        name_parts = name.split()
        last_name = name_parts[-1]
        first_letters = "".join([unidecode.unidecode(part[0]).lower() for part in name_parts[:-1]])
        
        # Generate username and email
        user_id_str = str(user_id)
        username = unidecode.unidecode(last_name).lower() + first_letters + user_id_str
        email = f"{unidecode.unidecode(last_name).lower()}{first_letters}{user_id_str}@user.libma"
        
        return username, email
    
    # Account model methods remain unchanged
    @staticmethod
    def to_dict(user):
        """
        Convert user object to dictionary with account properties
        
        Args:
            user (User): User object
            
        Returns:
            dict: User data as dictionary with account properties
        """
        return {
            'user_id': user.user_id,
            'name': user.name,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'date_of_birth': user.date_of_birth,
            'role': user.role,
            'generated': getattr(user, 'generated', False)
        }
    
    @staticmethod
    def get_account_by_id(user_id):
        """
        Get user account by ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: User account data or None if not found
        """
        try:
            user = User.get_user_by_id(user_id)
            if user:
                # Add account properties
                user.generated = add_account._was_generated(user.username, user.name, user.user_id)
                return add_account.to_dict(user)
            return None
        except Exception as e:
            print(f"Error getting user account: {str(e)}")
            return None
    
    @staticmethod
    def _was_generated(username, name, user_id):
        """
        Check if username was auto-generated
        
        Args:
            username (str): Username to check
            name (str): User's full name
            user_id (int): User ID
            
        Returns:
            bool: True if username appears to be auto-generated
        """
        if not name or len(name.split()) < 2:
            return False
        
        name_parts = name.split()
        last_name = name_parts[-1]
        first_letters = "".join([unidecode.unidecode(part[0]).lower() for part in name_parts[:-1]])
        
        expected = unidecode.unidecode(last_name).lower() + first_letters + str(user_id)
        return username == expected

    
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

@staticmethod
def delete_user_from_db(user_id):
    """Delete a user from the database"""
    try:
        # Try to cast user_id to integer since it might be coming as a string
        user_id = int(user_id)
        
        result = Admin.delete_user(Admin, user_id)
        
        # If the result is None or False, consider it as failed
        if result is None or result is False:
            print(f"No user found with ID {user_id}")
            return False
        
        print(f"User {user_id} deleted successfully")
        return True
        
    except ValueError:
        print(f"Invalid user ID format: {user_id}")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Exception in delete_user_from_db: {e}")
        return False

