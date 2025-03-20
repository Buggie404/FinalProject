from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import sys
import os

# Bỏ cái path resolution này dô là ko có cho chuyển tab đc
# Path resolution to find modules
try:
    # Try to find correct path to Controller and Model files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)

    # Add possible paths
    possible_paths = [
        grandparent_dir,
        os.path.join(grandparent_dir, "LibraryManagementApp"),
        parent_dir,
        current_dir
    ]

    for path in possible_paths:
        if path not in sys.path:
            sys.path.append(path)

    # Import Controller
    from Controller.user_controller import add_account
except ModuleNotFoundError:
    try:
        # Try alternative import path
        from Controller.user_controller import add_account
    except ModuleNotFoundError:
        messagebox.showerror("Import Error", "Failed to import controller module. Please check your project structure.")
        sys.exit(1)

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
        self.load_image("image_2", (577.0, 93.0))

        # Create form fields with their respective icons
        self.create_entry_with_icon("lnE_Name", "image_3", (542.0, 121.0, 273.0, 46.0), (678.5, 145.0), (326.0, 145.0))
        self.create_entry_with_icon("lnE_User", "image_4", (542.0, 195.0, 273.0, 46.0), (678.5, 219.0), (318.0, 218.0))
        self.create_entry_with_icon("lnE_Email", "image_5", (542.0, 269.0, 273.0, 46.0), (678.5, 293.0), (324.0, 293.0))
        self.create_entry_with_icon("lnE_Password", "image_6", (542.0, 343.0, 273.0, 46.0), (678.5, 367.0), (343.0, 366.0))
        self.create_entry_with_icon("lnE_DateOfBirth", "image_7", (542.0, 417.0, 273.0, 46.0), (678.5, 441.0), (356.0, 441.0))

        # Set read-only for auto-generated fields
        self.entries["lnE_User"].configure(bg="#E7DCDC", relief="flat", readonlybackground="#E7DCDC")
        self.entries["lnE_Email"].configure(bg="#E7DCDC", relief="flat", readonlybackground="#E7DCDC")
        
        # Add placeholder for date field
        self.date_placeholder = "YY/MM/DD"
        self.entries["lnE_DateOfBirth"].insert(0, self.date_placeholder)
        self.entries["lnE_DateOfBirth"].config(fg="grey")  # Set placeholder text color to grey
        
        # Bind focus events for date field
        self.entries["lnE_DateOfBirth"].bind("<FocusIn>", self.on_date_field_focus_in)
        self.entries["lnE_DateOfBirth"].bind("<FocusOut>", self.on_date_field_focus_out)

        # Bind name field to generate username and email on Enter key press
        self.entries["lnE_Name"].bind("<Return>", self.generate_user_info)
        self.entries["lnE_Name"].bind("<FocusOut>", self.generate_user_info)

        # Create submit button
        self.create_button("btn_Confirm", (421.0, 486.0, 313.0, 48.0))

        # self.setup_date_field_placeholders()
        self.setup_field_events()
    
    def setup_field_events(self):
        """Set up focus and key events for form fields"""
        # Set up date field placeholders
        date_field = self.entries["lnE_DateOfBirth"]
        date_field.bind("<FocusIn>", self.on_date_field_focus_in)
        date_field.bind("<FocusOut>", self.on_date_field_focus_out)
        
        # Bind name field to generate username and email on Enter key press
        name_field = self.entries["lnE_Name"]
        name_field.bind("<Return>", self.generate_user_info)
        name_field.bind("<FocusOut>", self.generate_user_info)

    def on_date_field_focus_in(self, event):
        """Clear placeholder when date field gets focus"""
        if self.entries["lnE_DateOfBirth"].get() == self.date_placeholder:
            self.entries["lnE_DateOfBirth"].delete(0, "end")
            self.entries["lnE_DateOfBirth"].config(fg="#000716")  # Change to normal text color

    def on_date_field_focus_out(self, event):
        """Restore placeholder when date field loses focus if empty"""
        if not self.entries["lnE_DateOfBirth"].get():
            self.entries["lnE_DateOfBirth"].insert(0, self.date_placeholder)
            self.entries["lnE_DateOfBirth"].config(fg="grey")  # Change back to placeholder color

    def generate_user_info(self, event):
        """Generate username, email, and set default password"""
        name = self.entries["lnE_Name"].get().strip()
        if name:
            # Get next user ID 
            user_id = add_account.get_next_user_id()
            
            # Generate username and email
            username, email = add_account.generate_username_and_email(name, user_id)
            
            if username and email:
                # Set username and email
                self.entries["lnE_User"].delete(0, "end")
                self.entries["lnE_Email"].delete(0, "end")
                
                self.entries["lnE_User"].insert(0, username)
                self.entries["lnE_Email"].insert(0, email)
                
                # Set default password
                self.entries["lnE_Password"].delete(0, "end")
                self.entries["lnE_Password"].insert(0, "123456789")

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
    
    def validate_and_create_user(self):
        """Validate the form and create a new user"""
        name = self.entries["lnE_Name"].get().strip()
        username = self.entries["lnE_User"].get().strip()
        email = self.entries["lnE_Email"].get().strip()
        password = self.entries["lnE_Password"].get().strip()
        date_of_birth = self.entries["lnE_DateOfBirth"].get().strip()
        
        # Validate all fields
        valid, error_msg = add_account.validate_all_fields(name, username, email, date_of_birth)
        
        if not valid:
            messagebox.showerror("Validation Error", error_msg)
            return False
            
        # Check if password is empty
        if not password:
            messagebox.showerror("Validation Error", "Password cannot be empty.")
            return False
            
        # Create user
        success, message = add_account.create_user(name, username, email, password, date_of_birth)
        
        if success:
            messagebox.showinfo("Success", message)
            return True
        else:
            messagebox.showerror("Error", message)
            return False

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
            self.root.destroy()
            from UserAddAccount1 import UserAddAccount1App
            add_user_1_root = Tk()
            add_user_1 = UserAddAccount1App(add_user_1_root)
            add_user_1_root.mainloop()
        else:
            self.root.destroy()
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