from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, StringVar
from tkinter import ttk
import tkinter as tk
import os
import sys

class UserManagementApp:
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

        # Add sample data for testing
        self.sample_users = [
            (1, "John Doe", "johndoe", "john@example.com", "1990-01-15", "admin"),
            (2, "Jane Smith", "janesmith", "jane@example.com", "1992-05-22", "user"),
            (3, "Michael Johnson", "michaelj", "michael@example.com", "1985-11-30", "user"),
            (4, "Sarah Williams", "sarahw", "sarah@example.com", "1988-07-14", "user"),
            (5, "David Brown", "davidb", "david@example.com", "1995-03-08", "admin"),
            (6, "Emily Davis", "emilyd", "emily@example.com", "1991-09-17", "user"),
            (7, "Robert Wilson", "robertw", "robert@example.com", "1987-12-25", "user"),
            (8, "Jennifer Moore", "jenniferm", "jennifer@example.com", "1993-06-11", "user"),
            (9, "Thomas Taylor", "thomast", "thomas@example.com", "1989-02-28", "user"),
            (10, "Lisa Anderson", "lisaa", "lisa@example.com", "1994-08-19", "admin")
        ]

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()
        self.create_tbl_User()
        
        # Load sample data into the table
        self.load_sample_data()

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

    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Create a temporary logo placeholder
        self.canvas.create_rectangle(
            81.0, 24.0, 181.0, 124.0,
            fill="#FFFFFF", outline=""
        )
        self.canvas.create_text(
            131.0, 74.0,
            text="LOGO",
            fill="#0A66C2",
            font=("Montserrat Bold", 16)
        )

        # Create sidebar buttons with text
        self.create_text_button("Add Account", 131.0, 193.5, "#FFFFFF", "#0A66C2", "add_account")
        self.create_text_button("Edit Account", 131.0, 231.5, "#FFFFFF", "#0A66C2", "edit_account")
        self.create_text_button("Back to Homepage", 131.0, 575.5, "#FFFFFF", "#0A66C2", "back_to_homepage")

    def create_text_button(self, text, x, y, text_color, hover_color, command_name):
        """Create a text button in the sidebar"""
        btn_bg = self.canvas.create_rectangle(
            0.0, y - 12.5, 262.0, y + 12.5,
            fill="#0A66C2", outline="", tags=f"btn_{command_name}"
        )
        
        btn_text = self.canvas.create_text(
            x, y,
            text=text,
            fill=text_color,
            font=("Montserrat Bold", 12),
            tags=f"btn_{command_name}"
        )
        
        # Add hover effect
        def on_enter(e):
            self.canvas.itemconfig(btn_bg, fill=hover_color)
            self.canvas.itemconfig(btn_text, fill="#0A66C2" if text_color == "#FFFFFF" else "#FFFFFF")
            
        def on_leave(e):
            self.canvas.itemconfig(btn_bg, fill="#0A66C2")
            self.canvas.itemconfig(btn_text, fill=text_color)
            
        def on_click(e):
            print(f"{command_name} clicked")
            if command_name == "add_account":
                self.add_account()
            elif command_name == "edit_account":
                self.edit_account()
            elif command_name == "back_to_homepage":
                self.back_to_homepage()
                
        self.canvas.tag_bind(f"btn_{command_name}", "<Enter>", on_enter)
        self.canvas.tag_bind(f"btn_{command_name}", "<Leave>", on_leave)
        self.canvas.tag_bind(f"btn_{command_name}", "<Button-1>", on_click)

    def create_main_panel(self):
        """Create the main panel elements"""
        # Create title
        self.canvas.create_text(
            335.0, 38.0,
            text="User Management",
            fill="#000000",
            font=("Montserrat Bold", 24)
        )
        
        # Create search entry
        self.canvas.create_rectangle(
            578.0, 34.0, 871.0, 62.0,
            fill="#F0F0F0", outline="", tags="search_bg"
        )
        
        self.entry_search = Entry(
            self.root,
            bd=0,
            bg="#F0F0F0",
            fg="#000000",
            highlightthickness=0,
            font=("Montserrat", 12)
        )
        self.entry_search.place(
            x=588.0, y=38.0,
            width=273.0, height=20.0
        )
        
        # Set placeholder text
        self.entry_search.insert(0, "Search...")
        self.entry_search.config(fg="grey")
        
        def on_focus_in(event):
            if self.entry_search.get() == "Search...":
                self.entry_search.delete(0, "end")
                self.entry_search.config(fg="black")
                
        def on_focus_out(event):
            if self.entry_search.get() == "":
                self.entry_search.insert(0, "Search...")
                self.entry_search.config(fg="grey")
                
        def on_search(event):
            search_term = self.entry_search.get().lower()
            if search_term and search_term != "search...":
                self.search_users(search_term)
                
        self.entry_search.bind("<FocusIn>", on_focus_in)
        self.entry_search.bind("<FocusOut>", on_focus_out)
        self.entry_search.bind("<Return>", on_search)
        
        # Create delete button
        self.btn_delete = Button(
            self.root,
            text="Delete Account",
            font=("Montserrat Bold", 12),
            bg="#0A66C2",
            fg="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_account,
            state="disabled"
        )
        self.btn_delete.place(
            x=719.0, y=533.0,
            width=152.0, height=43.0
        )

    def create_tbl_User(self):
        """Create the user table using ttk.Treeview"""
        # Configure the ttk style
        style = ttk.Style()
        
        # Configure the Treeview style
        style.configure(
            "Treeview",
            background="#E6E6E6",
            foreground="black",
            fieldbackground="#E6E6E6",
            font=("Montserrat", 11)
        )
        
        # Configure the Treeview.Heading style
        style.configure(
            "Treeview.Heading",
            background="#D3D3D3",
            foreground="black",
            font=("Montserrat Bold", 12)
        )
        
        # Style when a row is selected
        style.map('Treeview', 
            background=[('selected', '#0A66C2')],
            foreground=[('selected', 'white')]
        )
        
        # Create a frame to hold the treeview and scrollbar
        table_frame = Frame(self.root)
        table_frame.place(x=285.0, y=121.0, width=586.0, height=386.0)
        
        # Create the treeview
        self.tbl_User = ttk.Treeview(
            table_frame,
            selectmode="browse",
            columns=("user_id", "name", "username", "email", "date_of_birth", "role"),
            show="headings"
        )

        # Create the scrollbar
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tbl_User.yview)
        self.tbl_User.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        
        # Define column headings and widths
        columns = {
            "user_id": ("User ID", 50),
            "name": ("Name", 100),
            "username": ("Username", 100),
            "email": ("Email", 120),
            "date_of_birth": ("Date of Birth", 100),
            "role": ("Role", 70)
        }
        
        # Configure each column
        for col_id, (col_name, col_width) in columns.items():
            self.tbl_User.heading(col_id, text=col_name, anchor="w")
            self.tbl_User.column(col_id, width=col_width, anchor="w")
        
        # Pack the treeview
        self.tbl_User.pack(side="left", fill="both", expand=1)
        
        # Bind the selection event
        self.tbl_User.bind("<<TreeviewSelect>>", self.on_user_select)
        
        # Bind a click on column header for sorting
        for col in columns:
            self.tbl_User.heading(col, command=lambda _col=col: self.sort_treeview_column(_col))

    def load_sample_data(self):
        """Load sample data into the table for demonstration"""
        # Clear any existing data
        for item in self.tbl_User.get_children():
            self.tbl_User.delete(item)
            
        # Insert sample user data
        for user in self.sample_users:
            self.tbl_User.insert('', 'end', values=user)

    def try_load_user_data(self):
        """Try to load real user data if possible (fallback to sample data)"""
        try:
            # Try to find the correct path to the Model directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            grandparent_dir = os.path.dirname(parent_dir)
            
            # Add possible paths to sys.path
            possible_paths = [
                grandparent_dir,
                os.path.join(grandparent_dir, "LibraryManagementApp"),
                parent_dir,
                current_dir
            ]
            
            for path in possible_paths:
                if path not in sys.path:
                    sys.path.append(path)
            
            # Try to import User model
            from Model.user_model import User
            
            # Clear existing data
            for item in self.tbl_User.get_children():
                self.tbl_User.delete(item)
                
            # Load user data from database
            users = User.get_all_user()
            if users:
                for user in users:
                    self.tbl_User.insert('', 'end', values=(
                        user[0],  # user_id
                        user[1],  # name
                        user[2],  # username
                        user[3],  # email
                        user[5],  # date_of_birth (skipping password at index 4)
                        user[6]   # role
                    ))
                return True
            return False
            
        except Exception as e:
            print(f"Error loading user data: {e}")
            return False

    def search_users(self, search_term):
        """Search users by the search term"""
        # Clear selection
        for item in self.tbl_User.selection():
            self.tbl_User.selection_remove(item)
            
        # Remove highlights
        for item in self.tbl_User.get_children():
            self.tbl_User.item(item, tags=())
            
        # Search and highlight matching items
        found = False
        for item in self.tbl_User.get_children():
            values = self.tbl_User.item(item, 'values')
            for value in values:
                if value and search_term in str(value).lower():
                    self.tbl_User.item(item, tags=('found',))
                    self.tbl_User.tag_configure('found', background='#ADD8E6')
                    found = True
                    break
                    
        if not found:
            print(f"No users found matching '{search_term}'")

    def sort_treeview_column(self, col):
        """Sort the treeview content when a column header is clicked"""
        if not hasattr(self, 'sort_direction'):
            self.sort_direction = {}
            
        current_direction = self.sort_direction.get(col, 'asc')
        reverse = (current_direction == 'asc')
        
        if col == "user_id":
            # For user_id, sort as integers
            data = [(int(self.tbl_User.set(iid, col)), iid) for iid in self.tbl_User.get_children('')]
        elif col == "role":
            # For the role column, sort with admin first, then user
            data = []
            for iid in self.tbl_User.get_children(''):
                role = self.tbl_User.set(iid, col)
                # Sort key: 0 for admin, 1 for user, 2 for anything else
                sort_key = 0 if role.lower() == "admin" else (1 if role.lower() == "user" else 2)
                data.append((sort_key, iid))
        else:
            # For other columns, sort as strings
            data = [(self.tbl_User.set(iid, col), iid) for iid in self.tbl_User.get_children('')]
            
        # Sort the data
        data.sort(reverse=reverse)
        
        # Rearrange items in sorted positions
        for idx, (_, iid) in enumerate(data):
            self.tbl_User.move(iid, '', idx)
            
        # Update sort direction for next click
        self.sort_direction[col] = 'desc' if current_direction == 'asc' else 'asc'

    def on_user_select(self, event):
        """Handle user selection event"""
        selected_items = self.tbl_User.selection()
        if selected_items:
            selected_item = selected_items[0]
            user_data = {
                'user_id': self.tbl_User.item(selected_item, 'values')[0],
                'name': self.tbl_User.item(selected_item, 'values')[1],
                'username': self.tbl_User.item(selected_item, 'values')[2],
                'email': self.tbl_User.item(selected_item, 'values')[3],
                'date_of_birth': self.tbl_User.item(selected_item, 'values')[4],
                'role': self.tbl_User.item(selected_item, 'values')[5]
            }
            print(f"Selected user: {user_data}")
            
            # Enable the delete button
            self.btn_delete.config(state='normal')
        
    def add_account(self):
        """Handle add account button click"""
        print("Add account functionality would be implemented here")
        # You would typically open a new dialog window here
        
    def edit_account(self):
        """Handle edit account button click"""
        selected_items = self.tbl_User.selection()
        if selected_items:
            selected_item = selected_items[0]
            user_data = {
                'user_id': self.tbl_User.item(selected_item, 'values')[0],
                'name': self.tbl_User.item(selected_item, 'values')[1],
                'username': self.tbl_User.item(selected_item, 'values')[2],
                'email': self.tbl_User.item(selected_item, 'values')[3],
                'date_of_birth': self.tbl_User.item(selected_item, 'values')[4],
                'role': self.tbl_User.item(selected_item, 'values')[5]
            }
            print(f"Edit account for: {user_data}")
            # You would typically open a dialog with the user's data pre-filled
        else:
            print("Please select a user to edit")
            
    def delete_account(self):
        """Handle delete account button click"""
        selected_items = self.tbl_User.selection()
        if selected_items:
            selected_item = selected_items[0]
            user_id = self.tbl_User.item(selected_item, 'values')[0]
            user_name = self.tbl_User.item(selected_item, 'values')[1]
            
            print(f"Deleting user {user_id}: {user_name}")
            
            # Remove from treeview
            self.tbl_User.delete(selected_item)
            
            # Update the list of sample users
            self.sample_users = [user for user in self.sample_users if user[0] != int(user_id)]
            
            # Disable the delete button after deletion
            self.btn_delete.config(state='disabled')
            
    def back_to_homepage(self):
        """Handle back to homepage button click"""
        print("Back to homepage clicked")
        # You would typically navigate back to the main application screen here
        
    def run(self):
        """Start the application main loop"""
        # First try to load actual user data from the database
        if not self.try_load_user_data():
            # If that fails, use sample data
            self.load_sample_data()
            
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    root.title("User Management")
    app = UserManagementApp(root)
    app.run()