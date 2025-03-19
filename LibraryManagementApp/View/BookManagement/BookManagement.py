from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, Frame


class BookManagementApp:
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

        # # Main content panel
        # self.tbl_Book = self.canvas.create_rectangle(
        #     285.0, 156.0, 871.0, 542.0,
        #     fill="#D9D9D9", outline=""
        # )

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
           font=("Montserrat", 10, "bold")
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
           "author": ("Author", 110),
           "published_year": ("Published Year", 70),
           "category": ("Category", 50),
           "quantity": ("Quantity", 50)
       }
      
       # Configure each column
       for col_id, (col_name, col_width) in columns.items():
           self.tbl_Book.heading(col_id, text=col_name, anchor="w")
           self.tbl_Book.column(col_id, width=col_width, anchor="w")
      
       # Pack the treeview
       self.tbl_Book.pack(side="left", fill="both", expand=1)
      
       # Bind the selection event
    #    self.tbl_Book.bind("<<TreeviewSelect>>", self.on_user_select)
      
       # Bind a click on column header for sorting
    #    for col in columns:
            # self.tbl_Book.heading(col, command=lambda _col=col: self.sort_treeview_column(_col))


    # def sort_treeview_column(self, col):
    #     """Sort the treeview content when a column header is clicked"""
    #     if col in ["book_id", "price", "quantity", "year"]:
    #         # Numeric columns should be sorted as numbers
    #         data = []
    #         for iid in self.tbl_Book.get_children(''):
    #             value = self.tbl_Book.set(iid, col)
    #             try:
    #                 # Convert to float for numeric sorting
    #                 numeric_value = float(value)
    #                 data.append((numeric_value, iid))
    #             except ValueError:
    #                 # If conversion fails, place at the beginning with value 0
    #                 data.append((0, iid))
    #         data.sort()
    #     elif col == "category":
    #         # For category column, sort with predefined category order
    #         category_order = {
    #             "fantasy": 0, 
    #             "fiction": 1, 
    #             "romance": 2, 
    #             "technology": 3, 
    #             "biography": 4
    #         }
            
    #         data = []
    #         for iid in self.tbl_Book.get_children(''):
    #             category = self.tbl_Book.set(iid, col).lower()
    #             # Get category priority, default to high number for unknown categories
    #             sort_key = category_order.get(category, 99)
    #             data.append((sort_key, iid))
    #         data.sort()
    #     else:
    #         # For other columns (title, author), sort alphabetically
    #         data = [(self.tbl_Book.set(iid, col), iid) for iid in self.tbl_Book.get_children('')]
    #         data.sort()
        
    #     # Rearrange items in sorted positions
    #     for idx, (_, iid) in enumerate(data):
    #         self.tbl_Book.move(iid, '', idx)
        
    #     # Set the sort direction for the next click
    #     if hasattr(self, 'sort_direction') and self.sort_direction.get(col) == 'asc':
    #         self.tbl_Book.delete(*self.tbl_Book.get_children())
    #         data.reverse()
    #         for _, iid in data:
    #             self.tbl_Book.move(iid, '', 'end')
    #         self.sort_direction[col] = 'desc'
    #     else:
    #         if not hasattr(self, 'sort_direction'):
    #             self.sort_direction = {}
    #         self.sort_direction[col] = 'asc'


if __name__ == "__main__":
    root = Tk()
    app = BookManagementApp(root)
    app.run()