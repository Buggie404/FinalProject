# """ To handle  Validation """
# # Import fetched data from Admin Model
# from Model.admin_model import Admin
# from Model.user_model import User
# from View.UserManagement import UserManagement

# class Search_users:
#     def __init__(self):
#         pass

#     @staticmethod
#     def search_by_id(user_id):
#         if not user_id:
#             return False, "There are no matching IDs!"

#         user = User.get_id(user_id)
#         if user:
#             return True, user
#         return False, "There are no matching IDs!"

#     @staticmethod
#     def search_by_username(username):
#         if not username:
#             return False, "There are no matching usernames!"

#         user = User.get_username(username)
#         if user:
#             return True, user
#         return False, "There are no matching usernames!"

""" To handle  Validation """
# Import fetched data from Admin Model
from Model.admin_model import Admin
from Model.user_model import User
from tkinter import messagebox
from View.noti_tab_view_1 import Message_1

class Search_users:
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