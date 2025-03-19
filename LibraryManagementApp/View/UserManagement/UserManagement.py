from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, StringVar
from tkinter import ttk
import tkinter as tk

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

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()
        self.create_user_table()  # Add the table creation

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

    def create_user_table(self):
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
            font=("Montserrat", 12, "bold")
        )
        
        # Configure the Treeview.Heading style
        style.configure(
            "Treeview.Heading",
            background="#E6E6E6",
            foreground="black",
            font=("Montserrat", 12, "bold")
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
        self.user_table = ttk.Treeview(
            table_frame,
            selectmode="browse",
            columns=("user_id", "name", "username", "email", "date_of_birth", "role"),
            show="headings"
        )

        # Create the scrollbar
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        self.user_table.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(x=586, y=0, width=15, height=386)
        
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
            self.user_table.heading(col_id, text=col_name, anchor="w")
            self.user_table.column(col_id, width=col_width, anchor="w")
        
        # Pack the treeview
        self.user_table.pack(side="left", fill="both", expand=1)
        
        # Bind the selection event
        self.user_table.bind("<<TreeviewSelect>>", self.on_user_select)
        
        # Bind a click on column header for sorting
        for col in columns:
            self.user_table.heading(col, command=lambda _col=col: self.sort_treeview_column(_col))

        

    def sort_treeview_column(self, col):
        """Sort the treeview content when a column header is clicked"""
        if col != "role":
            # For other columns, sort normally
            data = [(self.user_table.set(iid, col), iid) for iid in self.user_table.get_children('')]
            data.sort()
        else:
            # For the role column, sort with admin first, then user
            data = []
            for iid in self.user_table.get_children(''):
                role = self.user_table.set(iid, col)
                # Sort key: 0 for admin, 1 for user, 2 for anything else
                sort_key = 0 if role.lower() == "admin" else (1 if role.lower() == "user" else 2)
                data.append((sort_key, iid))
            data.sort()
            
        # Rearrange items in sorted positions
        for idx, (_, iid) in enumerate(data):
            self.user_table.move(iid, '', idx)
            
        # Set the sort direction for the next click
        if hasattr(self, 'sort_direction') and self.sort_direction.get(col) == 'asc':
            self.user_table.delete(*self.user_table.get_children())
            data.reverse()
            for _, iid in data:
                self.user_table.move(iid, '', 'end')
            self.sort_direction[col] = 'desc'
        else:
            if not hasattr(self, 'sort_direction'):
                self.sort_direction = {}
            self.sort_direction[col] = 'asc'

    def on_user_select(self, event):
        """Handle user selection event"""
        selected_items = self.user_table.selection()
        if selected_items:
            selected_item = selected_items[0]
            user_data = {
                'user_id': self.user_table.item(selected_item, 'values')[0],
                'name': self.user_table.item(selected_item, 'values')[1],
                'username': self.user_table.item(selected_item, 'values')[2],
                'email': self.user_table.item(selected_item, 'values')[3],
                'date_of_birth': self.user_table.item(selected_item, 'values')[4],
                'role': self.user_table.item(selected_item, 'values')[5]
            }
            print(f"Selected user: {user_data}")
            
            # You can enable the delete button here
            if 'btn_DeleteAccount' in self.buttons:
                self.buttons['btn_DeleteAccount'].config(state='normal')

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
        
        # Initially disable the delete button until a user is selected
        if button_name == "btn_DeleteAccount":
            button.config(state='disabled')

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
            selected_items = self.user_table.selection()
            if selected_items:
                selected_item = selected_items[0]
                print(f"Deleting user: {self.user_table.item(selected_item, 'values')}")
                self.user_table.delete(selected_item)
                # Disable the delete button after deletion
                self.buttons['btn_DeleteAccount'].config(state='disabled')

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = UserManagementApp(root)
    app.run()