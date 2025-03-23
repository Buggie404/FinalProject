from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, StringVar, messagebox
from tkinter import ttk
import tkinter as tk
import os
import sys

class UserManagementApp:
    def __init__(self, root, user_data = None, assets_path=None):
        # Initialize the main window
        self.root = root
        self.user_data = user_data
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
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameUserManagement")

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
        self.create_tbl_User()  # Add the table creation
        self.load_user()

    def relative_to_assets(self, path):
        """Helper function to get the absolute path to assets"""
        return self.assets_path / Path(path)

    def create_background(self):
        """Create the background elements"""
        # Sidebar background
        self.canvas.create_rectangle(
            0.0, 0.0, 262.0, 605.0,
            fill="#0A66C2", outline=""
        )
        
        # We remove the tbl_User rectangle as it will be replaced by the Treeview
        # self.tbl_User = self.canvas.create_rectangle(
        #    285.0, 121.0, 871.0, 507.0,
        #    fill="#F0F0F0", outline=""
        # )

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
        # Create search entry at top
        self.create_entry("lnE_Search", (578.0, 49.0), (305.0, 25.0, 546.0, 46.0), "#F0F0F0")

        # Create action button
        self.create_button("btn_DeleteAccount", (719.0, 533.0, 115.0, 43.0))

    def create_tbl_User(self):
        """Create the user table using ttk.Treeview"""
        # Configure the ttk style
        style = ttk.Style()
        # style.theme_use("classic")
        
        # Configure the Treeview style
        style.configure(
            "Treeview",
            background="#E6E6E6",
            foreground="black",
            fieldbackground="#E6E6E6",
            font=("Montserrat", 10, "normal")
        )
        
        # Configure the Treeview.Heading style
        style.configure(
            "Treeview.Heading",
            background="#E6E6E6",
            foreground="black",
            font=("Montserrat", 10, "bold")
        )
        
        # Style when a row is selected
        style.map('Treeview', 
            background=[('selected', '#0A66C2')],
            foreground=[('selected', 'white')]
        )
        
        # Create a frame to hold the treeview and scrollbar
        table_frame = Frame(self.root)
        table_frame.place(x=285.0, y=121.0, width=586.0, height=386.0)
        
        # Create the scrollbar
        vsb = ttk.Scrollbar(table_frame, orient='vertical')
        vsb.pack(side='right', fill='y')

        # Create the treeview
        self.tbl_User = ttk.Treeview(
            table_frame,
            yscrollcommand=vsb.set,
            selectmode="browse",
            columns=("user_id", "name", "username", "email", "date_of_birth", "role"),
            show="headings"
        )

        # Config scrollbar
        vsb.config(command=self.tbl_User.yview)
        
        # Define column headings and widths
        columns = {
            "user_id": ("User ID", 60),
            "name": ("Name", 100),
            "username": ("Username", 110),
            "email": ("Email", 120),
            "date_of_birth": ("Date of Birth", 90),
            "role": ("Role", 70)
        }
        
        # Configure each column
        for col_id, (col_name, col_width) in columns.items():
            self.tbl_User.heading(col_id, text=col_name, anchor="c")
            self.tbl_User.column(col_id, width=col_width, anchor="w")
        
        # Pack the treeview
        self.tbl_User.pack(side="left", fill="both", expand=1)
        
    def load_user(self):
        """ Try to load data if possible"""
        try:
            # Try to find correct path to Model file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            grandparent_dir = os.path.dirname(parent_dir)

            # Add possible path
            possible_paths = [
                grandparent_dir,
                os.path.join(grandparent_dir, "LibraryManagementApp"),
                parent_dir,
                current_dir
            ]

            for path in possible_paths:
                if path not in sys.path:
                    sys.path.append(path)

            from Model.user_model import User

             # Clear existing data
            for item in self.tbl_User.get_children():
                self.tbl_User.delete(item)
                
            # Load user data from database
            Users = User.get_all_user()
            if Users:
                for User in Users:
                    self.tbl_User.insert('', 'end', values=(
                        User[0],  # User_id
                        User[1],  # name
                        User[2],  # username
                        User[3],  # email
                        User[5],  # date_of_birth
                        User[6]  # role
                    ))
                return True
            return False

        except Exception as e:
            print(f"Error loading user data: {e}")
            return False
    


    def filter_by_user_id(self):
        """Filter the user table by user_id or username"""
        search_term = self.entries["lnE_Search"].get()
        
        try:
            # Import the controller
            from Controller.user_controller import Search_users
            
            # Call the controller's filter_users method that handles both ID and username
            Search_users.filter_users(
                self.tbl_User,  # The Treeview widget
                search_term,    # The search term
                self.load_user,  # The function to reload all users
                self.root       # Pass the root window for noti tab
            )
        except Exception as e:
            print(f"Error while filtering users: {e}")
            # Reload all users if filtering fails
            self.load_user()

        
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

    def create_entry(self, entry_name, bg_position, entry_dimensions, bg_color, placeholder="Search"):
        """Create an entry field with a placeholder"""
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
            bg=bg_color,
            fg="#000716",
            highlightthickness=0
        )

        # Set placeholder text
        entry.insert(0, placeholder)
        entry.config(fg="grey")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg="black")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="grey")

        # Add Enter key binding for search entry
        if entry_name == "lnE_Search":
            entry.bind("<Return>", lambda event: self.filter_by_user_id())

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        entry.place(
            x=entry_dimensions[0],
            y=entry_dimensions[1],
            width=entry_dimensions[2],
            height=entry_dimensions[3]
        )

        self.entries[entry_name] = entry

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")
        
        if button_name == "btn_DeleteAccount":
            from Controller.user_controller import Delete_Users
            from Model.admin_model import Admin
            from noti_tab_view_1 import Delete, Message_1, Invalid
            selected_items = self.tbl_User.selection()
            if not selected_items:
                messagebox.showinfo("Error", "Please select an account to delete.")
                return
                
            selected_item = selected_items[0]
            user_values = self.tbl_User.item(selected_item, 'values')
            
            if not user_values:
                messagebox.showinfo("Error", "No user data found.")
                return
                
            user_id = user_values[0]  # First column is user_id
            print(f"Attempting to delete user ID: {user_id}")

            # Define a direct callback function to handle deletion
            def confirm_delete_callback():
                print(f"Executing delete callback for user ID: {user_id}")
                try:
                    # Create admin and use its delete_user method
                    admin = Admin()
                    success = admin.delete_user(user_id)

                    if success:
                        print(f"Successfully deleted user ID: {user_id}")
                        # Remove from UI
                        self.tbl_User.delete(selected_item)
                        # Show success message
                        Message_1(self.root, "account")
                    else:
                        print(f"Failed to delete user ID: {user_id}")
                        messagebox.showerror("Error", "Failed to delete user")
                except Exception as e:
                    print(f"Error during deletion: {e}")
                    messagebox.showerror("Error", f"Error: {str(e)}")
            # Create delete confirmation dialog
            delete_dialog = Delete(self.root, "account")
            delete_dialog.set_yes_callback(confirm_delete_callback) 

        elif button_name == "btn_AddAccount":
            self.root.destroy()
            from UserAddAccount import UserAddAccountApp
            add_user_root = Tk()
            add_user = UserAddAccountApp(add_user_root, user_data = self.user_data)
            add_user_root.mainloop()
        elif button_name == 'btn_EditAccountPassword':
            self.root.destroy()
            from UserEditAccount import UserEditAccountApp
            edit_pass_root = Tk()
            edit_pass = UserEditAccountApp(edit_pass_root, user_data = self.user_data)
            edit_pass_root.mainloop()
        else:
            self.root.destroy()
            from Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role = self.role, user_data = self.user_data)
            homepage_root.mainloop()


    def run(self):
        """Start the application main loop"""
        self.root.mainloop()




if __name__ == "__main__":
    root = Tk()
    app = UserManagementApp(root)
    app.run()