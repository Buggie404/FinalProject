# Import Lib
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import os
import sys

# Import base file path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, "Model"))
sys.path.append(os.path.join(base_dir, "Controller"))
sys.path.append(base_dir)

# Import models and controllers
from Model.user_model import User
from Controller.account_management_controller import PasswordChangeController

class AccountChangePwApp:
    def __init__(self, root, user_data=None, assets_path=None):
        # Initialize the main window
        self.root = root
        self.user_data = user_data  # Store the user data from login
        
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        
        # Initialize the controller first, before using it
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
        
        # Add validation error text placeholders
        self.error_messages = {
            'current_password': None,
            'new_password': None,
            'confirm_password': None
        }
    
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
        self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill=color, outline=color)
        # Bo góc dưới bên phải
        self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill=color, outline=color)
        
        # Phần thân của hình chữ nhật
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)
    
    def create_background(self):
        """Create the background elements with rounded corners for the main panel"""
        # Sidebar (không cần bo góc)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            262.0,
            605.0,
            fill="#0A66C2",
            outline=""
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
        self.create_entry_with_icon("lnE_CurrentPassword", "image_2", (544.0, 181.0, 273.0, 46.0), (680.5, 205.0), (409.0, 204.0))
        self.create_entry_with_icon("lnE_NewPassword", "image_3", (544.0, 267.0, 273.0, 46.0), (680.5, 291.0), (409.0, 291.0))
        self.create_entry_with_icon("lnE_ConfirmPassword", "image_4", (544.0, 355.0, 273.0, 46.0), (680.5, 379.0), (409.0, 379.0))
        
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
    
    def on_current_password_focusout(self, event):
        """Handle focus out event for current password field"""
        current_password = self.entries["lnE_CurrentPassword"].get()
        valid, message, show_error = self.controller.validate_current_password_field(current_password)
        
        if show_error:
            messagebox.showerror("Password Error", message)
            self.entries["lnE_CurrentPassword"].focus_set()
    
    def on_new_password_focusout(self, event):
        """Handle focus out event for new password field"""
        new_password = self.entries["lnE_NewPassword"].get()
        valid, message, show_error = self.controller.validate_new_password_field(new_password)
        
        if show_error:
            messagebox.showerror("Password Error", message)
            self.entries["lnE_NewPassword"].focus_set()
    
    def on_confirm_password_focusout(self, event):
        """Handle focus out event for confirm password field"""
        new_password = self.entries["lnE_NewPassword"].get()
        confirm_password = self.entries["lnE_ConfirmPassword"].get()
        valid, message, show_error = self.controller.validate_confirm_password_field(new_password, confirm_password)
        
        if show_error:
            messagebox.showerror("Password Error", message)
            self.entries["lnE_ConfirmPassword"].focus_set()
    
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
            show="•" if "Password" in entry_name else ""
        )
        
        entry.place(
            x=entry_dimensions[0],
            y=entry_dimensions[1],
            width=entry_dimensions[2],
            height=entry_dimensions[3]
        )
        
        # Add validation bindings based on entry type
        if entry_name == "lnE_CurrentPassword":
            entry.bind("<FocusOut>", self.on_current_password_focusout)
        elif entry_name == "lnE_NewPassword":
            entry.bind("<FocusOut>", self.on_new_password_focusout)
        elif entry_name == "lnE_ConfirmPassword":
            entry.bind("<FocusOut>", self.on_confirm_password_focusout)
        
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
            
            # Process password change through controller
            success, message, redirect, field_to_focus = self.controller.process_password_change(
                current_password, new_password, confirm_password
            )
            
            if success:
                # Navigate to success screen
                self.root.destroy()
                from View.AccountManagement.AccountChangePassword1 import AccountChangePw1App
                success_root = Tk()
                success_app = AccountChangePw1App(success_root, user_data=self.controller.get_user_data())
                success_root.mainloop()
            else:
                # Show error message
                if not redirect:
                    messagebox.showerror("Password Error", message)
                    
                    # Set focus to appropriate field based on error
                    if field_to_focus == "current_password":
                        self.entries["lnE_CurrentPassword"].focus_set()
                    elif field_to_focus == "new_password":
                        self.entries["lnE_NewPassword"].focus_set()
                    elif field_to_focus == "confirm_password":
                        self.entries["lnE_ConfirmPassword"].focus_set()
                else:
                    # Navigate to failure screen
                    self.root.destroy()
                    from View.AccountManagement.AccountChangePassword2 import AccountChangePw2App
                    failure_root = Tk()
                    failure_app = AccountChangePw2App(failure_root, user_data=self.controller.get_user_data())
                    failure_root.mainloop()
        else:
            # Handle other navigation through controller
            self.controller.handle_navigation(button_name, self)
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = AccountChangePwApp(root)
    app.run()
