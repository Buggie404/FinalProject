from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Controller.book_edit_controller import BookEditController
from Model.book_model import Book  
from View.noti_tab_view_1 import Invalid


class BookManaEditBook:
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
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBookManaEditBook")

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
        self.create_rounded_rectangle(285.0, 56.0, 871.0, 244.0, radius=10, color="#F1F1F1")

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
        # Load title and other images
        self.load_image("image_3", (577.0, 78.0))
        self.load_image("image_2", (447.0, 132.0))

        # Create search field with entry
        self.create_entry("lnE_ISBN", (683.5, 132.5), (554.5, 116.0, 258.0, 31.0))

        # Create search button
        self.create_button("btn_Search", (421.0, 181.0, 313.0, 48.0))

        # Bind search button to search function
        if "btn_Search" in self.buttons:
            self.buttons["btn_Search"].config(command=self.search_book)

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

    def create_entry(self, entry_name, bg_position, dimensions):
        """Create an entry field with background image"""
        self.images[entry_name] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )

        # Create the background image for the entry
        self.canvas.create_image(
            bg_position[0],
            bg_position[1],
            image=self.images[entry_name]
        )

        # Create the actual entry widget
        entry = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )

        entry.place(
            x=dimensions[0],
            y=dimensions[1],
            width=dimensions[2],
            height=dimensions[3]
        )

        self.entries[entry_name] = entry

    # def button_click(self, button_name):
    #     """Handle button click events"""
    #     print(f"{button_name} clicked")

    # def run(self):
    #     """Start the application main loop"""
    #     self.root.mainloop()
    
    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")
        
        if button_name == "btn_BackToHomepage":
            self.root.destroy()
            from View.Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root)
            homepage_root.mainloop()
    
    def search_book(self):
        """Search for a book by ISBN and open edit screen if found"""
        if 'lnE_ISBN' not in self.entries:
            print("Error: ISBN entry field not found")
            return
            
        isbn = self.entries['lnE_ISBN'].get().strip()
        
        # Validate ISBN format
        if not isbn.isdigit() or len(isbn) != 13:
            Invalid(self.root, 'Input')
            return
            
        # Try to find the book
        book = Book.get_book_by_id(isbn)
        
        if not book:
            Invalid(self.root, 'search_book')
            return
            
        # Book found, navigate to edit screen
        self.root.destroy()
        
        # Create new edit screen
        edit_root = Tk()
        from View.BookManagement.BookManaEditBook1 import BookEdit1App
        edit_app = BookEdit1App(edit_root, book_data=book)
        edit_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = BookManaEditBook(root)
    app.run()