""" To handle Log In Validation """
# Import fetched data from User Model
from Model.user_model import User
from View.LogIn import LogInApp 

class Authen():
    def __init__ (self):
        pass

    @staticmethod
    def check_account_login(email, password):
        # Validate input is not empty
        if not email or not password:
            return False, None

        # Use the User model to check credentials
        user_data = User.login(email, password)

        # If user_data is None, login failed
        if user_data is None:
            return False, None

        # Return success and the user data
        return True, user_data
    
    @staticmethod
    def check_account_role(email):
        # To check account role 
        user_data = User.get_user_by_email(email)