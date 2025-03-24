from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import os
import sys

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the View directory
parent_dir = os.path.dirname(current_dir)
# Go up one more level to the project root directory
project_root = os.path.dirname(parent_dir)
# Add project root to sys.path
sys.path.append(project_root)
from Controller.user_controller import add_account
from Model.user_model import User

class UserAddAccountApp:
    def __init__(self, root, user_data=None, assets_path=None, role=None):
        # Initialize the main window
        self.root = root
        self.user_data = user_data
        self.role=role
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        if self.user_data and len(self.user_data) > 6 and self.user_data[6] == "Admin":
            self.role = "admin"
        else:
            self.role = None or "user"

        # Set up asset paths
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameUserAddAccount")

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

    def relative_to_assets(self, path):
        """Helper function to get the absolute path to assets"""
        return self.assets_path / Path(path)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, color):
        """Vẽ hình chữ nhật có bo góc."""
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
        """Tạo nền chính với bo góc"""
        # Sidebar (không cần bo góc)
        self.canvas.create_rectangle(
            0.0, 0.0, 262.0, 605.0,
            fill="#0A66C2", outline=""
        )

        # Hình chữ nhật lớn nằm ngang (bo góc)
        self.create_rounded_rectangle(285.0, 59.0, 871.0, 547.0, radius=10, color="#F1F1F1")

    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Load and place logo
        self.load_image("image_1", (130.0, 74.0))

        # Create sidebar buttons
        self.create_button("btn_AddAccount", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditAccountPassword", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        """Create the main panel elements"""
        # Load title image
        self.load_image("image_2", (577.0, 102.0))

        # Create form fields with their respective icons
        self.create_entry_with_icon("lnE_Name", "image_3", (542.0, 164.0, 273.0, 46.0), (678.5, 188.0), (409.0, 188.0))
        self.create_entry_with_icon("lnE_Role", "image_4", (542.0, 267.0, 273.0, 46.0), (678.5, 291.0), (409.0, 291.0))
        self.create_entry_with_icon("lnE_DateOfBirth", "image_5", (542.0, 370.0, 273.0, 46.0), (678.5, 394.0), (409.0, 394.0))
        
        # Add placeholder for date field
        self.date_placeholder = "YYYY/MM/DD"
        self.entries["lnE_DateOfBirth"].insert(0, self.date_placeholder)
        self.entries["lnE_DateOfBirth"].config(fg="grey")  # Set placeholder text color to grey

        # Add placeholder for name field
        self.name_placeholder = "Full Name"
        self.entries["lnE_Name"].insert(0, self.name_placeholder)
        self.entries["lnE_Name"].config(fg="grey") # Set placeholder text color to grey

        # Add placeholder for role field
        self.role_placeholder = "User/Admin"
        self.entries["lnE_Role"].insert(0, self.role_placeholder)
        self.entries["lnE_Role"].config(fg="grey") # Set placeholder text color to grey

        # Create submit button
        self.create_button("btn_Confirm", (421.0, 473.0, 313.0, 48.0))

        # Setup field events for placeholders
        self.setup_field_events()
        
        # Initialize warning flags
        for field in ["lnE_Name", "lnE_Role", "lnE_DateOfBirth"]:
            self.entries[field]._shown_warning = False
    
    def setup_field_events(self):
        """Set up focus and key events for form fields"""
        # Set up field placeholders and events
        fields = {
            "lnE_DateOfBirth": self.date_placeholder,
            "lnE_Role": self.role_placeholder,
            "lnE_Name": self.name_placeholder
        }
        
        for field_name, placeholder in fields.items():
            if field_name in self.entries:
                self.entries[field_name].bind("<FocusIn>", self.on_input_field_focus_in)
                self.entries[field_name].bind("<FocusOut>", self.on_input_field_focus_out)
                self.entries[field_name].bind("<KeyRelease>", self.on_input_field_change)
    
    def on_input_field_change(self, event):
        """Reset warning flag when field content changes"""
        widget = event.widget
        widget._shown_warning = False
    
    def on_input_field_focus_in(self, event):
        """Clear placeholder text when field receives focus"""
        widget = event.widget
        
        if widget == self.entries["lnE_DateOfBirth"]:
            if widget.get() == self.date_placeholder:
                widget.delete(0, "end")
                widget.config(fg="#000716")  # Change to normal text color
            # Reset warning flag when user starts editing
            widget._shown_warning = False
        
        elif widget == self.entries["lnE_Role"]:
            if widget.get() == self.role_placeholder:
                widget.delete(0, "end")
                widget.config(fg="#000716")  # Change to normal text color
            # Reset warning flag when user starts editing
            widget._shown_warning = False
        
        elif widget == self.entries["lnE_Name"]:
            if widget.get() == self.name_placeholder:
                widget.delete(0, "end")
                widget.config(fg="#000716")  # Change to normal text color
            # Reset warning flag when user starts editing
            widget._shown_warning = False

    def on_input_field_focus_out(self, event):
        """Restore placeholder text if field is empty and validate field content."""
        widget = event.widget

        # Define mapping of fields to their attributes
        field_mapping = {
            "lnE_Name": (self.name_placeholder, add_account.validate_name_on_event),
            "lnE_Role": (self.role_placeholder, add_account.validate_role_on_event),
            "lnE_DateOfBirth": (self.date_placeholder, add_account.validate_date_on_event)
        }

        # Identify which field triggered the event
        for field_name, (placeholder, validation_func) in field_mapping.items():
            if widget == self.entries[field_name]:
                field_value = widget.get()

                # Restore placeholder if empty
                if not field_value:
                    widget.insert(0, placeholder)
                    widget.config(fg="grey")
                    widget._shown_warning = False  # Reset warning flag when placeholder is restored
                    return

                # Validate field only if flag is not set
                valid, message = validation_func(field_value)

                if not valid:
                    # Show warning only if not already shown
                    if not widget._shown_warning:
                        messagebox.showwarning(f"Invalid {field_name.split('_')[-1]}", message)
                        widget._shown_warning = True  # Set flag to prevent duplicate warnings
                        # Schedule focus to happen after the messagebox is closed
                        self.root.after(100, lambda w=widget: w.focus_set())
                    else:
                        # Even if we've shown the warning before, still keep focus on this field
                        widget.focus_set()
                else:
                    widget._shown_warning = False  # Reset flag if validation passes
                break  # Exit loop after handling the matched field

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
        entry_image = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )
        self.images[f"{entry_name}_bg"] = entry_image

        self.canvas.create_image(
            bg_position[0],
            bg_position[1],
            image=entry_image
        )

        entry = Entry(
            bd=0,
            bg="#E7DCDC",
            fg="#000716",
            highlightthickness=0
        )

        entry.place(
            x=entry_dimensions[0],
            y=entry_dimensions[1],
            width=entry_dimensions[2],
            height=entry_dimensions[3]
        )

        self.entries[entry_name] = entry
        self.load_image(icon_name, icon_position)

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")

        if button_name == "btn_Confirm":
            # Temporarily disable FocusOut validation to avoid duplicate triggers
            for field_name in ["lnE_Name", "lnE_Role", "lnE_DateOfBirth"]:
                self.entries[field_name].unbind("<FocusOut>")
            
            # Allow safe focus change without triggering validation
            self.root.focus_set()
            
            # Retrieve values from entry fields
            name = self.entries["lnE_Name"].get()
            role = self.entries["lnE_Role"].get()
            date_of_birth = self.entries["lnE_DateOfBirth"].get()
            
            # Skip if placeholders are detected
            if name == self.name_placeholder:
                self.root.after(100, lambda: self.entries["lnE_Name"].focus_set())
            elif role == self.role_placeholder:
                self.root.after(100, lambda: self.entries["lnE_Role"].focus_set())
            elif date_of_birth == self.date_placeholder:
                self.root.after(100, lambda: self.entries["lnE_DateOfBirth"].focus_set())
                
            # Process the form if all validations pass
            success, message, user_data = add_account.process_user_form(name, role, date_of_birth)

            # In UserAddAccount.py - Modify the button_click method (btn_Confirm section)
            if success:
                self.root.destroy()
                from UserAddAccount1 import UserAddAccount1App
                user_management_root = Tk()
                user_management = UserAddAccount1App(user_management_root, user_data['user_id'],  user_data=self.user_data, role=self.role)  # Pass user_id
                user_management_root.mainloop()
            else:
                messagebox.showerror("Error", message)
                # Determine which field to focus based on the error message
                if "name" in message.lower():
                    self.root.after(100, lambda: self.entries["lnE_Name"].focus_set())
                elif "role" in message.lower():
                    self.root.after(100, lambda: self.entries["lnE_Role"].focus_set())
                elif "date" in message.lower() or "birth" in message.lower():
                    self.root.after(100, lambda: self.entries["lnE_DateOfBirth"].focus_set())
        
        elif button_name == "btn_AddAccount":
            self.root.destroy()
            from View.UserManagement.UserManagement import UserManagementApp
            add_user_root = Tk()
            add_user = UserManagementApp(add_user_root, user_data=self.user_data)
            add_user_root.mainloop()
        
        elif button_name == 'btn_EditAccountPassword':
            self.root.destroy()
            from UserEditAccount import UserEditAccountApp
            edit_pass_root = Tk()
            edit_pass = UserEditAccountApp(edit_pass_root, user_data=self.user_data)
            edit_pass_root.mainloop()
        
        else:  # btn_BackToHomepage
            self.root.destroy()
            from Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role=self.role, user_data=self.user_data)
            homepage_root.mainloop()

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = UserAddAccountApp(root)
    app.run()