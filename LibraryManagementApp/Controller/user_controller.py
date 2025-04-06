""" To handle any function related to user management """
# Import fetched data from Admin Model
from tkinter import messagebox
from View.noti_tab_view_1 import Delete, Message_1, Message_2, Invalid
from tkinter import messagebox
import re
import datetime
import unidecode
import os
import sys

from Model.admin_model import Admin
from Model.user_model import User

# Add parent directory to path to import from Model
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

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
            date_of_birth (str): Date of birth in format YYYY-MM-DD
            
        Returns:
            tuple: (success_flag, message, user_data)
        """
        # Reset validation errors for a fresh form submission
        field_errors = {
            'name': False,
            'role': False,
            'date_of_birth': False
        }
        
        # Format and validate name (auto-convert to Title Case)
        formatted_name = add_account.format_name(name)
        valid_name, name_msg = add_account.validate_name(formatted_name)
        if not valid_name:
            field_errors['name'] = True
            
        # Format and validate role (auto-convert to proper case)
        formatted_role = add_account.format_role(role)
        valid_role, role_msg, formatted_role = add_account.validate_role(formatted_role)
        if not valid_role:
            field_errors['role'] = True
            
        # Format and validate date (handle different formats)
        formatted_date = add_account.format_date_input(date_of_birth)
        valid_date, date_msg = add_account.validate_date_format(formatted_date)
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
        
        try:
            username, email = add_account.generate_username_and_email(formatted_name, user_id, formatted_role)
            if not username or not email:
                return False, "Could not generate username and email. Please check the name format.", {}
        except Exception as e:
            return False, f"Error generating username and email: {str(e)}", {}
        
        # Format date for database (already in YYYY-MM-DD format now)
        db_date = formatted_date
        
        # Create user data dictionary
        user_data = {
            'user_id': user_id,
            'name': formatted_name,
            'username': username,
            'email': email,
            'password': add_account.default_password,
            'date_of_birth': db_date,
            'role': formatted_role
        }
        
        # Create and save user directly without separate UserAccount class
        try:
            user = User(
                user_id=user_id, 
                name=formatted_name, 
                username=username, 
                email=email, 
                password=add_account.default_password, 
                date_of_birth=db_date, 
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
    def format_name(name):
        """
        Format name to Title Case
        
        Args:
            name (str): Name to format
            
        Returns:
            str: Name formatted in Title Case
        """
        if not name or name.strip() == "":
            return ""
        
        # Split name into parts and title each part
        name_parts = name.strip().split()
        formatted_parts = [part.capitalize() for part in name_parts]
        
        # Join parts back together
        return " ".join(formatted_parts)
    
    @staticmethod
    def format_role(role):
        """
        Format role to proper case ('User' or 'Admin')
        
        Args:
            role (str): Role to format
            
        Returns:
            str: Formatted role
        """
        if not role or role.strip() == "":
            return ""
        
        role_lower = role.strip().lower()
        
        # Check if role matches exactly "user" or "admin" (case insensitive)
        if role_lower == "user":
            return "User"
        elif role_lower == "admin":
            return "Admin"
        else:
            return role
    
    @staticmethod
    def format_date_input(date_text):
        """
        Format date input to YYYY-MM-DD format, rejecting non-numeric characters
        
        Args:
            date_text (str): Date text to format
            
        Returns:
            str: Date in YYYY-MM-DD format or original input if invalid format detected
        """
        if not date_text or date_text.strip() == "":
            return ""
        
        # First check if input contains only numbers and separators (hyphens or slashes)
        if not re.match(r'^[0-9/-]+$', date_text.strip()):
            return date_text  # Return original to trigger validation error
        
        # Remove any characters that are not numbers, hyphens, or slashes
        cleaned_date = re.sub(r'[^0-9/-]', '', date_text.strip())
        
        # Check if date is already in YYYY-MM-DD format
        if re.match(r'^(\d{4})-(\d{2})-(\d{2})$', cleaned_date):
            return cleaned_date
            
        # Try to handle YYYY/MM/DD format
        if re.match(r'^(\d{4})/(\d{2})/(\d{2})$', cleaned_date):
            year, month, day = cleaned_date.split('/')
            return f"{year}-{month}-{day}"
            
        # Try to handle other common formats like DD/MM/YYYY or MM/DD/YYYY
        if '/' in cleaned_date and len(cleaned_date.split('/')) == 3:
            parts = cleaned_date.split('/')
            
            # If one part is a 4-digit year, assume it's the year
            for i, part in enumerate(parts):
                if len(part) == 4 and part.isdigit():
                    year = part
                    remaining = [p for j, p in enumerate(parts) if j != i]
                    
                    # Assume month then day (could be improved with more logic)
                    month, day = remaining
                    
                    # Ensure two digits for month and day
                    month = month.zfill(2)
                    day = day.zfill(2)
                    
                    return f"{year}-{month}-{day}"
            
            # If no 4-digit year found, assume last part is year and add century if needed
            day, month, year = parts
            if len(year) == 2:
                current_year = datetime.datetime.now().year
                century = str(current_year)[:2]
                year = century + year
                
            # Ensure two digits for month and day
            month = month.zfill(2)
            day = day.zfill(2)
            
            return f"{year}-{month}-{day}"
            
        # For hyphen format (YYYY-MM-DD or DD-MM-YYYY)
        if '-' in cleaned_date and len(cleaned_date.split('-')) == 3:
            parts = cleaned_date.split('-')
            
            # If first part is a 4-digit number, assume YYYY-MM-DD
            if len(parts[0]) == 4 and parts[0].isdigit():
                return cleaned_date  # Already in correct format
                
            # Otherwise assume DD-MM-YYYY
            day, month, year = parts
            
            # Add century if needed
            if len(year) == 2:
                current_year = datetime.datetime.now().year
                century = str(current_year)[:2]
                year = century + year
                
            # Ensure two digits for month and day
            month = month.zfill(2)
            day = day.zfill(2)
            
            return f"{year}-{month}-{day}"
        
        # If all else fails, return the original (validation will catch errors)
        return cleaned_date
    
    @staticmethod
    def validate_name_on_event(name):
        """
        Format and validate name field when focus leaves the field
        
        Args:
            name (str): Name to validate
            
        Returns:
            tuple: (is_valid, error_message, formatted_name)
        """
        formatted_name = add_account.format_name(name)
        valid, message = add_account.validate_name(formatted_name)
        add_account.field_validation_errors['name'] = not valid
        return valid, message, formatted_name
    
    @staticmethod
    def validate_role_on_event(role):
        """
        Format and validate role field when focus leaves the field
        
        Args:
            role (str): Role to validate
            
        Returns:
            tuple: (is_valid, error_message, formatted_role)
        """
        formatted_role = add_account.format_role(role)
        valid, message, formatted_role = add_account.validate_role(formatted_role)
        add_account.field_validation_errors['role'] = not valid
        return valid, message, formatted_role
    
    @staticmethod
    def validate_date_on_event(date_text):
        """
        Format and validate date field when focus leaves the field
        
        Args:
            date_text (str): Date to validate
            
        Returns:
            tuple: (is_valid, error_message, formatted_date)
        """
        formatted_date = add_account.format_date_input(date_text)
        valid, message = add_account.validate_date_format(formatted_date)
        add_account.field_validation_errors['date_of_birth'] = not valid
        return valid, message, formatted_date
    
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
        Validate that role is exactly 'User' or 'Admin'
        
        Args:
            role (str): Role to validate
            
        Returns:
            tuple: (is_valid, error_message, formatted_role)
        """
        if not role or role.strip() == "":
            return False, "Role cannot be empty.", ""
        
        formatted_role = add_account.format_role(role)
        
        # Check if role is exactly "User" or "Admin" after formatting
        if formatted_role in ["User", "Admin"]:
            return True, "", formatted_role
        else:
            return False, "Role must be either 'User' or 'Admin'.", ""
    
    @staticmethod
    def validate_date_format(date_text):
        """
        Validate date format (YYYY-MM-DD), check if it contains only numbers and separators, 
        and check if user is at least 10 years old
        
        Args:
            date_text (str): Date text to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not date_text or date_text.strip() == "":
            return False, "Date of birth cannot be empty."
        
        # First check if input contains only numbers and separators (hyphens or slashes)
        if not re.match(r'^[0-9/-]+$', date_text.strip()):
            return False, "Date must contain only numbers and date separators (- or /)."
        
        try:
            # Check format
            if not re.match(r'^(\d{4})-(\d{2})-(\d{2})$', date_text):
                return False, "Invalid date format. Use YYYY-MM-DD."
            
            # Parse date
            year, month, day = date_text.split('-')
            
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
            
            # Check if user is at least 10 years old
            current_date = datetime.datetime.now()
            age = current_date.year - date_obj.year - ((current_date.month, current_date.day) < (date_obj.month, date_obj.day))
            
            if age < 10:
                return False, "User must be at least 10 years old."
                
            return True, ""
            
        except ValueError:
            return False, "Invalid date. Please use YYYY-MM-DD format."
    
    @staticmethod
    def get_next_user_id():
        """
        Get the next available user ID from the database
        
        Returns:
            int: Next available user ID
        """
        try:
            users = User.get_all_user()
            if not users:
                return 1  # Default if no users
                
            # Get all existing user IDs and sort them
            existing_ids = sorted([int(user[0]) for user in users])
            
            # Return next ID after the highest
            next_id = existing_ids[-1] + 1
            return next_id
        except Exception as e:
            print(f"Error getting next user ID: {str(e)}")
            return 167  # Default fallback value
    
    @staticmethod
    def generate_username_and_email(name, user_id, role):
        """
        Generate username and email based on full name, user ID, and role
        
        Args:
            name (str): Full name of the user
            user_id (int): User ID
            role (str): User role ('User' or 'Admin')
            
        Returns:
            tuple: (username, email)
        """
        if not name or len(name.split()) < 2:
            return None, None
        
        name_parts = name.split()
        last_name = name_parts[-1]
        first_letters = "".join([unidecode.unidecode(part[0]).lower() for part in name_parts[:-1]])
        
        # Ensure 4-digit user ID with leading zeros
        user_id_str = f"{user_id:04d}"  # This guarantees 4 digits with leading zeros
        
        username = unidecode.unidecode(last_name).lower() + first_letters + f"{user_id:04d}"
        
        # Determine email domain based on role
        email = f"{unidecode.unidecode(last_name).lower()}{first_letters}{user_id_str}@{'admin' if role == 'Admin' else 'user'}.libma"
        
        return username, email
    
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
    def __init__(self, view, admin):
        self.view = view
        self.admin = admin
        self.selected_user_id = None

    def on_user_select(self, event):
        """Handle user selection in the table"""
        selected_items = self.view.tbl_User.selection()
        if selected_items:
            item = self.view.tbl_User.item(selected_items[0])
            self.selected_user_id = item["values"][0]
        else:
            self.selected_user_id = None

    def delete_selected_user(self):
        """Show delete confirmation dialog and handle deletion"""
        if not self.selected_user_id:
            Invalid(self.view.root, "account")
            return

        # Create delete confirmation dialog
        delete_dialog = Delete(self.view.root, "account")
        delete_dialog.set_yes_callback(self.confirm_delete_user)

    def confirm_delete_user(self):
        """Delete the selected user from database and UI"""
        if not self.admin:
            try:
                from Model.admin_model import Admin
                self.admin = Admin(None, None)
            except Exception as e:
                print(f" Failed to create admin: {e}")
                return

        user_id_to_delete = self.selected_user_id

        selected_items = self.view.tbl_User.selection()
        selected_item = selected_items[0] if selected_items else None

        if not selected_item:
            return

        # Delete user from database
        success = self.delete_user_from_db(user_id_to_delete)

        if success:
            self.view.tbl_User.delete(selected_item)
            Message_1(self.view.root, "account")
            self.selected_user_id = None
        else:
            Invalid(self.view.root, "database error")

    @staticmethod
    def delete_user_from_db(user_id):
        """Delete a user from the database by ID"""
        try:
            result = User.delete_user(user_id)
            return result
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

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
                current_role = getattr(root_window, 'role', 'user')
                current_user_data = getattr(root_window, 'user_data', None)
                # Display success message với role và user_data
                Message_2(root_window, 'pass_reset', user_data=current_user_data, role=current_role)
                return True
            else:
                # Display error message
                Message_1(root_window, 'edit_pass_id')
                return False
                
        except Exception as e:
            print(f"Error resetting password: {e}")
            import traceback
            traceback.print_exc()
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
            user_details = self.get_user_details(user_id)
            
            if user_details:
                # Get the current role and user_data - first check on root_window directly
                current_role = getattr(root_window, 'role', None)
                current_user_data = getattr(root_window, 'user_data', None)
                
                # If not found, try accessing through the app instance
                if current_role is None and hasattr(root_window, '_nametowidget'):
                    for widgetname in root_window.winfo_children():
                        widget = root_window.nametowidget(str(widgetname))
                        if hasattr(widget, 'role'):
                            current_role = widget.role
                        if hasattr(widget, 'user_data'):
                            current_user_data = widget.user_data
                
                # check if user is admin
                if current_role is None and current_user_data and len(current_user_data) > 6:
                    if current_user_data[6] == "Admin":
                        current_role = "admin"
                    else:
                        current_role = "user"
                
                # Close current window
                root_window.destroy()
                
                # Create new window with user data
                reset_1_root = Tk()
                
                # Pass the role and user_data explicitly
                reset_1 = UserEditAccount1App(reset_1_root, user_data=current_user_data, role=current_role)
                
                # Force the role value if we know it's an admin
                if current_user_data and len(current_user_data) > 6 and current_user_data[6] == "Admin":
                    reset_1.role = "admin"
                
                # Update the labels with user data
                reset_1_root.update()
                
                # Now update the text of the labels
                reset_1.canvas.itemconfig(reset_1.lbl_ID, text=str(user_details['user_id']))
                reset_1.canvas.itemconfig(reset_1.lbl_Name, text=user_details['name'])
                reset_1.canvas.itemconfig(reset_1.lbl_EmailAddress, text=user_details['email'])
                reset_1.canvas.itemconfig(reset_1.lbl_Username, text=user_details['username'])
                
                # Store the user_id for later use when resetting password
                reset_1.current_user_id = user_details['user_id']
                
                # Add command to reset password button
                reset_1.buttons["btn_ResetPassword"].config(
                    command=lambda: self.reset_user_password(reset_1.current_user_id, reset_1_root)
                )
                
                reset_1_root.mainloop()
                return True
                
        except Exception as e:
            print(f"Error switching to UserEditAccount1: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return False