from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, Frame

import sys
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the View directory
parent_dir = os.path.dirname(current_dir)

# Go up one more level to the project root directory
project_root = os.path.dirname(parent_dir)

# Add project root to sys.path
sys.path.append(project_root)

# Now import using the package path
from Controller.book_management_controller import DeleteBook

class BookManagementApp:
    def __init__(self, root, assets_path=None, admin_user=None, role=None):
        # Initialize the main window
        self.root = root
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        self.admin_user = admin_user
        self.role = role

        # Set up asset paths
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBookManagement")

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
        self.buttons = {}
        self.entries = {}

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()

        # Create book table
        self.create_book_table()
        
        # Load book data into the table
        self.load_book()

        # Update UI based on user role
        self.update_ui_based_on_role()

        # Initialize controller AFTER all UI elements are created
        self.controller = DeleteBook(self)
        
        # Set admin user in the controller
        if self.admin_user:
            self.controller.set_admin(self.admin_user)

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

    def update_ui_based_on_role(self):
        """Show or hide buttons based on user role"""
        admin_buttons = ["btn_AddBook", "btn_EditBookInformation", "btn_DeleteBook"]
        
        if self.role != "admin":
            # Nếu không phải admin, ẩn các nút admin
            for button_name in admin_buttons:
                if button_name in self.buttons:
                    self.buttons[button_name].place_forget()

    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Load and place logo
        self.load_image("image_1", (131.0, 74.0))

        # Create sidebar buttons
        self.create_button("btn_AddBook", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditBookInformation", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        """Create the main panel elements"""
        # Create search entry
        self.create_entry("lnE_SearchBook", (578.0, 49.0), (305.0, 25.0, 546.0, 46.0), "#EEEBEB")

        # Create action buttons
        self.create_button("btn_Fantasy", (285.0, 88.0, 103.0, 43.0))
        self.create_button("btn_Fiction", (403.0, 88.0, 103.0, 43.0))
        self.create_button("btn_Romance", (521.0, 88.0, 103.0, 43.0))
        self.create_button("btn_Technology", (639.0, 88.0, 103.0, 43.0))
        self.create_button("btn_Biography", (757.0, 88.0, 103.0, 43.0))
        self.create_button("btn_DeleteBook", (719.0, 552.0, 115.0, 43.0))

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
        if button_name == "btn_DeleteBook":
            selected_items = self.tbl_Book.selection()
            if selected_items:
                selected_item = selected_items[0]
                print(f"Deleting book: {self.tbl_Book.item(selected_item, 'values')}")
                self.tbl_Book.delete(selected_item)

        if button_name == "btn_AddBook":
            self.root.destroy()
            from View.BookManagement.BookManaAddBook import BookManagementAddBookApp
            add_book_root = Tk()
            add_book = BookManagementAddBookApp(add_book_root)
            add_book.mainloop()

        if button_name == "btn_EditBookInformation":
            self.root.destroy()
            from View.BookManagement.BookManaEditBook import BookManaEditBook
            edit_book_root = Tk()
            edit_book = BookManaEditBook(edit_book_root)
            edit_book.mainloop()
        
        if button_name == "btn_BackToHomepage":
            self.root.destroy()
            from View.Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role = self.admin_user)
            homepage.mainloop()

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()
    
    def create_book_table(self):
       """Create the user table using ttk.Treeview"""
       # Configure the ttk style
       style = ttk.Style()
      
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
           background="#D3D3D3",
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
       table_frame.place(x=285.0, y=156.0, width=586.0, height=386.0)
      
       # Create the scrollbar
       vsb = ttk.Scrollbar(table_frame, orient="vertical")
       vsb.pack(side='right', fill='y')
      
       # Create the treeview
       self.tbl_Book = ttk.Treeview(
           table_frame,
           yscrollcommand=vsb.set,
           selectmode="browse",
           columns=("book_id", "title", "author", "published_year", "category", "quantity"),
           show="headings"
       )
      
       # Configure the scrollbar
       vsb.config(command=self.tbl_Book.yview)
      
       # Define column headings and widths
       columns = {
           "book_id": ("ISBN", 60),
           "title": ("Title", 110),
           "author": ("Author", 70),
           "published_year": ("Published Year", 70),
           "category": ("Category", 50),
           "quantity": ("Quantity", 50)
       }
      
       # Configure each column
       for col_id, (col_name, col_width) in columns.items():
           self.tbl_Book.heading(col_id, text=col_name, anchor="c")
           self.tbl_Book.column(col_id, width=col_width, anchor="w")
      
       # Pack the treeview
       self.tbl_Book.pack(side="left", fill="both", expand=1)

    def load_book(self):
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
            from Model.book_model import Book
            
            # Clear existing data
            for item in self.tbl_Book.get_children():
                self.tbl_Book.delete(item)
                
            # Load user data from database
            books = Book.get_all_book()
            if books:
                for book in books:
                    book_id = str(book[0])
                    self.tbl_Book.insert('', 'end', values=(
                        book_id,          # book_id (as string)
                        book[1],          # title
                        book[2],          # author
                        book[3],          # published_year
                        book[4],          # category
                        book[5]           # quantity
                    ))
                return True
            return False
            
        except Exception as e:
            print(f"Error loading user data: {e}")
            return False

if __name__ == "__main__":
    root = Tk()
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(parent_dir)
    from Model.admin_model import Admin
    admin_user = Admin()
    app = BookManagementApp(root, admin_user=admin_user, role="admin")
    app.run()