# Import Lib
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import os
import sys

# Import base file path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, "Model"))
sys.path.append(os.path.join(base_dir, "Controller"))
# sys.path.append(os.path.join(base_dir, "View"))
sys.path.append(base_dir)

# Import models and controllers
from Model.user_model import User
from Controller.password_change_controller import PasswordChangeController

class AccountChangePwApp:
    def __init__(self, root, user_data=None, assets_path=None):
        # Initialize the main window
        self.root = root
        self.user_data = user_data  # Store the user data from login
        self.password_validation_errors = {
            'current_password': False,
            'new_password': False,
            'confirm_password': False
        }

        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        # Initialize the controller first, before using it
        from Controller.password_change_controller import PasswordChangeController
        self.controller = PasswordChangeController(user_data)

        # Set up asset paths
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameAccountChangePassword")

        # Create canvas
        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=605,
            width=898,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Store images and UI elements as instance variables
        self.images = {}
        self.entries = {}
        self.buttons = {}

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()

        # # Add validation error text placeholders
        # self.error_messages = {
        #     'current_password': None,
        #     'new_password': None,
        #     'confirm_password': None
        # }

    def relative_to_assets(self, path):
        """Helper function to get the absolute path to assets"""
        return self.assets_path / Path(path)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, color):
        """Vẽ hình chữ nhật có bo góc"""
        # Bo góc trên bên trái
        self.canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, fill=color, outline=color)
        # Bo góc trên bên phải
        self.canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, fill=color, outline=color)
        # Bo góc dưới bên trái
        self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill=color,
                               outline=color)
        # Bo góc dưới bên phải
        self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill=color,
                               outline=color)

        # Phần thân của hình chữ nhật
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)

    def create_background(self):
        """Create the background elements with rounded corners for the main panel"""
        # Sidebar (không cần bo góc)
        self.canvas.create_rectangle(
            0.0, 0.0, 262.0, 605.0,
            fill="#0A66C2", outline=""
        )

        # Hình chữ nhật lớn nằm ngang (bo góc)
        self.create_rounded_rectangle(285.0, 80.0, 871.0, 525.0, radius=10, color="#F1F1F1")

    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Load and place logo
        self.load_image("image_5", (131.0, 74.0))

        # Create sidebar buttons
        self.create_button("btn_ChangePassword", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditAccountInformation", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        """Create the main panel elements"""
        # Title image
        self.load_image("image_1", (577.0, 120.0))

        # Create entry fields with icons
        self.create_entry_with_icon("lnE_CurrentPassword", "image_2", (544.0, 181.0, 273.0, 46.0), (680.5, 205.0),
                                    (409.0, 204.0))
        self.create_entry_with_icon("lnE_NewPassword", "image_3", (544.0, 267.0, 273.0, 46.0), (680.5, 291.0),
                                    (409.0, 291.0))
        self.create_entry_with_icon("lnE_ConfirmPassword", "image_4", (544.0, 355.0, 273.0, 46.0), (680.5, 379.0),
                                    (409.0, 379.0))

        # Create confirm button
        self.create_button("btn_ChangePasswordConfirm", (421.0, 448.0, 313.0, 48.0))

    def load_image(self, image_name, position):
        """Load an image and place it on the canvas"""
        self.images[image_name] = PhotoImage(
            file=self.relative_to_assets(f"{image_name}.png")
        )
        self.canvas.create_image(
            position[0],
            position[1],
            image=self.images[image_name]
        )

    def validate_current_password_event(self, event):
        """Validate current password when focus leaves the field"""
        current_password = self.entries["lnE_CurrentPassword"].get()
        valid, message = self.controller.validate_current_password(current_password)
        self.password_validation_errors['current_password'] = not valid
        
        # Update or create error message
        if not valid:
            messagebox.showerror("Password Error", message)
        
        return valid

    def validate_new_password_event(self, event):
        """Validate new password when focus leaves the field"""
        new_password = self.entries["lnE_NewPassword"].get()
        valid, message = self.controller.validate_new_password(new_password)
        self.password_validation_errors['new_password'] = not valid
        
        if not valid:
            messagebox.showerror("Password Error", message)
        
        return valid

    def validate_confirm_password_event(self, event):
        """Validate confirm password when focus leaves the field"""
        new_password = self.entries["lnE_NewPassword"].get()
        confirm_password = self.entries["lnE_ConfirmPassword"].get()
        valid, message = self.controller.validate_confirm_password(new_password, confirm_password)
        self.password_validation_errors['confirm_password'] = not valid
        
        if not valid:
            messagebox.showerror("Password Error", message)
        
        return valid


    def create_button(self, button_name, dimensions):
        """Create a button with the given name and dimensions"""
        self.images[button_name] = PhotoImage(
            file=self.relative_to_assets(f"{button_name}.png")
        )

        button = Button(
            image=self.images[button_name],
            borderwidth=0,
            highlightthickness=0,
            command=lambda b=button_name: self.button_click(b),
            relief="flat"
        )

        button.place(
            x=dimensions[0],
            y=dimensions[1],
            width=dimensions[2],
            height=dimensions[3]
        )

        self.buttons[button_name] = button

    def create_entry_with_icon(self, entry_name, icon_name, entry_dimensions, bg_position, icon_position):
        """Create an entry field with an icon"""
        self.images[entry_name] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )
        self.canvas.create_image(
            bg_position[0],
            bg_position[1],
            image=self.images[entry_name]
        )

        entry = Entry(
            bd=0,
            bg="#E7DCDC",
            fg="#000716",
            highlightthickness=0,
            show="•"
        )

        entry.place(
            x=entry_dimensions[0],
            y=entry_dimensions[1],
            width=entry_dimensions[2],
            height=entry_dimensions[3]
        )

        # Add validation bindings based on entry type
        if entry_name == "lnE_CurrentPassword":
            entry.bind("<FocusOut>", self.validate_current_password_event)
        elif entry_name == "lnE_NewPassword":
            entry.bind("<FocusOut>", self.validate_new_password_event)
        elif entry_name == "lnE_ConfirmPassword":
            entry.bind("<FocusOut>", self.validate_confirm_password_event)

        self.entries[entry_name] = entry
        self.load_image(icon_name, icon_position)

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")
        if button_name == "btn_ChangePasswordConfirm":
            # Get values from entry fields
            current_password = self.entries["lnE_CurrentPassword"].get()
            new_password = self.entries["lnE_NewPassword"].get()
            confirm_password = self.entries["lnE_ConfirmPassword"].get()
            
            # Create event objects for validation
            class DummyEvent:
                pass
            
            event = DummyEvent()
            
            # Validate all fields
            current_valid = self.validate_current_password_event(event)
            new_valid = self.validate_new_password_event(event)
            confirm_valid = self.validate_confirm_password_event(event)
            
            # Check if current password is correct and new password is valid
            if current_valid and new_valid and confirm_valid:
                # Update password in database
                success = self.controller.change_password(new_password)
                
                if success:
                    # Navigate to success screen
                    self.root.destroy()
                    from View.AccountManagement.AccountChangePassword1 import AccountChangePw1App
                    success_root = Tk()
                    success_app = AccountChangePw1App(success_root, user_data=self.controller.user_data)
                    success_root.mainloop()
                else:
                    # Navigate to failure screen due to database error
                    self.root.destroy()
                    from View.AccountManagement.AccountChangePassword2 import AccountChangePw2App
                    failure_root = Tk()
                    failure_app = AccountChangePw2App(failure_root, user_data=self.controller.user_data)
                    failure_root.mainloop()
            else:
                # Navigate to failure screen due to validation errors
                self.root.destroy()
                from View.AccountManagement.AccountChangePassword2 import AccountChangePw2App
                failure_root = Tk()
                failure_app = AccountChangePw2App(failure_root, user_data=self.controller.user_data)
                failure_root.mainloop()

        # if button_name == "btn_ChangePassword": # When clicked Change Password on Change Password window -> go back to Account MainWindow
        #     self.root.destroy()
        #     from AccountMan import AccountManagement
        #     accountman_root = Tk()
        #     accountman = AccountManagement(accountman_root)
        #     accountman_root.mainloop()
        # elif button_name == "btn_EditAccountInformation":
        #     self.root.destroy()
        #     from AccountEditInfo import AccountEditInfoApp
        #     editinfo_root = Tk()
        #     editinfo = AccountEditInfoApp(editinfo_root)
        #     editinfo_root.mainloop()
        # elif button_name == "btn_BackToHomepage":
        #     self.root.destroy()
        #     from Homepage import HomepageApp
        #     homepage_root = Tk()
        #     homepage = HomepageApp(homepage_root)
        #     homepage_root.mainloop()
        # # else: # For btn_ChangePasswordConfirm
        # """ changepass_success: check for new_password input, in Controller folder
        # if input of lnE_CurrentPassword ≠ user_password: -> Failed
        # if input of lnE_NewPassword ≠ input of lnE_ConfrimPassword: -> Failed"""
        # #     import Controller that handle the check for password validation
        # #     if changepass_success: # If password changed successfully -> switch to ChangePassword1 window -> update new_password in database through user_model
        # #     else: # Switch to AccountChangePassword2

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = AccountChangePwApp(root)
    app.run()