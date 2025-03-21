"""Handle password change functionality"""
import os
import sys
import re

# Set up path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, "Model"))
sys.path.append(os.path.join(base_dir, "View"))

from Model.user_model import User

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
    
    def validate_current_password(self, current_password):
        """Validate that current password matches the user's actual password"""
        if not current_password:
            return False, "Current password cannot be empty."
        
        if self.user_data and current_password != self.user_data[4]:
            return False, "Current password is incorrect."
        
        return True, ""
    
    def validate_new_password(self, new_password):
        """Validate new password requirements"""
        if not new_password:
            return False, "New password cannot be empty."
        
        # Check length (8-15 characters)
        if len(new_password) < 8:
            return False, "Password must be at least 8 characters."
        
        if len(new_password) > 15:
            return False, "Password must be less than 15 characters."
        
        # Check for spaces
        if ' ' in new_password:
            return False, "Password cannot contain spaces."
        
        # Check for valid characters
        valid_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*_-+=`|\\(){}[]:;'<>,.?/"
        for char in new_password:
            if char not in valid_chars:
                return False, f"Password contains invalid character: {char}"
        
        return True, ""
    
    def validate_confirm_password(self, new_password, confirm_password):
        """Validate that confirm password matches new password"""
        if not confirm_password:
            return False, "Confirm password cannot be empty."
        
        if new_password != confirm_password:
            return False, "Passwords do not match."
        
        return True, ""
    
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
