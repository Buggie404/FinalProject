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

class UserAddAccountApp:
    def __init__(self, root, assets_path=None):
        # Initialize the main window
        self.root = root
        self.root.geometry("898x605")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

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
    
    def on_input_field_focus_in(self, event):
        """Clear placeholder text when field receives focus"""
        widget = event.widget
        
        if widget == self.entries["lnE_DateOfBirth"] and widget.get() == self.date_placeholder:
            widget.delete(0, "end")
            widget.config(fg="#000716")  # Change to normal text color
        
        elif widget == self.entries["lnE_Role"] and widget.get() == self.role_placeholder:
            widget.delete(0, "end")
            widget.config(fg="#000716")  # Change to normal text color
        
        elif widget == self.entries["lnE_Name"] and widget.get() == self.name_placeholder:
            widget.delete(0, "end")
            widget.config(fg="#000716")  # Change to normal text color

    def on_input_field_focus_out(self, event):
        """Restore placeholder text if field is empty when it loses focus"""
        widget = event.widget
        
        if widget == self.entries["lnE_DateOfBirth"] and not widget.get():
            widget.insert(0, self.date_placeholder)
            widget.config(fg="grey")  # Change back to placeholder color

        elif widget == self.entries["lnE_Role"] and not widget.get():
            widget.insert(0, self.role_placeholder)
            widget.config(fg="grey")  # Change back to placeholder color
        
        elif widget == self.entries["lnE_Name"] and not widget.get():
            widget.insert(0, self.name_placeholder)
            widget.config(fg="grey")  # Change back to placeholder color

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

        if button_name == "btn_AddAccount":
            self.root.destroy()
            from UserManagement import UserManagementApp
            add_user_root = Tk()
            add_user = UserManagementApp(add_user_root)
            add_user_root.mainloop()
        elif button_name == 'btn_EditAccountPassword':
            self.root.destroy()
            from UserEditAccount import UserEditAccountApp
            edit_pass_root = Tk()
            edit_pass = UserEditAccountApp(edit_pass_root)
            edit_pass_root.mainloop()
        elif button_name == "btn_Confirm":
            # Get values from form fields
            name = self.entries["lnE_Name"].get()
            role = self.entries["lnE_Role"].get()
            date_of_birth = self.entries["lnE_DateOfBirth"].get()
            
            # Remove placeholder values if they're still there
            if name == self.name_placeholder:
                name = ""
            if role == self.role_placeholder:
                role = ""
            if date_of_birth == self.date_placeholder:
                date_of_birth = ""
            
            # Initialize controller
            controller = add_account()
            
            # Process the form data using the controller
            success, message, user_data = controller.process_user_form(name, role, date_of_birth)
            
            if success:
                # Show success message with user information
                message_text = f"{message}\n\nUsername: {user_data.get('username')}\nEmail: {user_data.get('email')}\nPassword: {user_data.get('password')}"
                messagebox.showinfo("Account Created", message_text)
                
                # Navigate to next screen
                self.root.destroy()
                from UserManagement import UserManagementApp
                user_management_root = Tk()
                user_management = UserManagementApp(user_management_root)
                user_management_root.mainloop()
            else:
                # Show error message
                messagebox.showerror("Error", message)
        else:  # btn_BackToHomepage
            self.root.destroy()
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.append(parent_dir)
            from Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root)
            homepage_root.mainloop()
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = UserAddAccountApp(root)
    app.run()