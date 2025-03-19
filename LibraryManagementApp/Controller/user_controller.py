""" To handle any function related to user management """
# Import fetched data from Admin Model
from Model.admin_model import Admin
from Model.user_model import User
from tkinter import messagebox

import re
import datetime
import unidecode
import os
import sys

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
                # Show error message
                messagebox.showinfo("Search Result", result)
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
            else:
                print(f"Filtering by username: {search_term}")
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
                from View.noti_tab_view_1 import Message_1
                Message_1(root, "search_account")
                load_user_func()
                
        except Exception as e:
            print(f"Error filtering users: {e}")
            # Reload all users if filtering fails
            load_user_func()

class add_account:
    @staticmethod
    def generate_username_and_email(name, user_id):
        """Generate username and email based on full name and user ID"""
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
    
    @staticmethod
    def validate_name(name):
        """Validate that name contains only letters and spaces"""
        if not name:
            return False, "Name cannot be empty."
        
        # Check for numbers or special characters
        if re.search(r'[^a-zA-ZÀ-ỹ\s]', name):
            return False, "Name should contain only letters and spaces."
        
        return True, ""
    
    @staticmethod
    def validate_date_format(date_text):
        """Validate date format (yy/mm/dd)"""
        if date_text == "yy/mm/dd" or not date_text:
            return False, "Please enter a valid date."
        
        # Allow only numbers and / character
        if re.search(r'[^0-9/]', date_text):
            return False, "Date should contain only numbers and / character."
        
        try:
            # Check format
            if not re.match(r'^(\d{2})/(\d{2})/(\d{2})$', date_text):
                return False, "Invalid date format. Use yy/mm/dd."
            
            # Parse date
            year, month, day = date_text.split('/')
            
            # Add century prefix to year
            if len(year) == 2:
                year = "20" + year  # Assuming 21st century
            
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
            return False, "Invalid date. Please use yy/mm/dd format."
    
    @staticmethod
    def format_date_for_database(date_text):
        """Convert date from yy/mm/dd to yyyy-mm-dd for database"""
        if not date_text or date_text == "yy/mm/dd":
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
        """Get the next available user ID from the database"""
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
    def create_user(name, username, email, password, date_of_birth):
        """Create a new user after validation"""
        try:
            # Format date for database
            formatted_date = add_account.format_date_for_database(date_of_birth)
            if not formatted_date:
                return False, "Invalid date format"
                
            # Create user object
            user = User(name=name, username=username, email=email, 
                        password=password, date_of_birth=formatted_date)
            
            # Save user to database
            user.save_user()
            return True, "User account created successfully!"
            
        except Exception as e:
            return False, f"Error creating user: {str(e)}"
    
    @staticmethod
    def validate_all_fields(name, username, email, date_of_birth):
        """Validate all fields before form submission"""
        # Validate name
        name_valid, name_msg = add_account.validate_name(name)
        if not name_valid:
            return False, name_msg
        
        # Check if username and email were generated
        if not username or not email:
            return False, "Username and email were not properly generated. Please check the name field."
        
        # Validate date of birth
        date_valid, date_msg = add_account.validate_date_format(date_of_birth)
        if not date_valid:
            return False, date_msg
        
        return True, ""