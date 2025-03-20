from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


class BookManagementAddBookApp:
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
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBookManaAddBook")

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
        self.create_form_elements()
        self.create_action_buttons()

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
        self.create_rounded_rectangle(285.0, 39.0, 875.0, 567.0, radius=10, color="#F1F1F1")

    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Load and place logo
        self.load_image("image_1", (131.0, 74.0))

        # Create sidebar buttons
        self.create_button("btn_AddBook", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditBookInformation", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        """Create the main panel header"""
        # Load header image
        self.load_image("image_2", (581.0, 69.0))

    def create_form_elements(self):
        """Create form labels and entry fields"""
        # Labels for the form fields
        label_positions = [
            ("image_3", (335.0, 124.0)),  # ISBN
            ("image_4", (335.0, 192.0)),  # Title
            ("image_5", (344.0, 260.0)),  # Author
            ("image_8", (379.0, 328.0)),  # Published year
            ("image_6", (353.0, 396.0)),  # Category
            ("image_7", (351.0, 464.0))  # Quantity
        ]

        for label_name, position in label_positions:
            self.load_image(label_name, position)

        # Entry fields
        entry_fields = [
            ("lnE_ISBN", (679.5, 124.0), (543.0, 100.0, 273.0, 46.0)),  # ISBN
            ("lnE_Title", (679.5, 192.0), (543.0, 168.0, 273.0, 46.0)),  # Title
            ("lnE_Author", (679.5, 260.0), (543.0, 236.0, 273.0, 46.0)),  # Author
            ("lnE_PublishedYear", (679.5, 328.0), (543.0, 304.0, 273.0, 46.0)),  # Published Year
            ("lnE_Category", (679.5, 396.0), (543.0, 372.0, 273.0, 46.0)),  # Category
            ("lnE_Quantity", (679.5, 464.0), (543.0, 440.0, 273.0, 46.0))  # Quantity
        ]

        for entry_name, image_pos, dimensions in entry_fields:
            self.create_entry(entry_name, image_pos, dimensions, "#E7DCDC")

    def create_action_buttons(self):
        """Create action buttons"""
        # Add Book button
        self.create_button("btn_Confirm", (425.0, 508.0, 313.0, 48.0))

    def load_image(self, image_name, position):
        """Load an image and place it on the canvas"""
        self.images[image_name] = PhotoImage(
            file=self.relative_to_assets(f"{image_name}.png")
        )

        image = self.canvas.create_image(
            position[0],
            position[1],
            image=self.images[image_name]
        )

        return image

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
        return button

    def create_entry(self, entry_name, image_position, dimensions, bg_color):
        """Create an entry field with the given parameters"""
        self.images[entry_name] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )

        entry_bg = self.canvas.create_image(
            image_position[0],
            image_position[1],
            image=self.images[entry_name]
        )

        entry = Entry(
            bd=0,
            bg=bg_color,
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
        return entry

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")

    def add_book(self):
        """Handle the add book functionality"""
        # Get values from entry fields
        book_name = self.entries["lnE_ISBN"].get()
        author = self.entries["lnE_Title"].get()
        isbn = self.entries["lnE_Author"].get()
        pub_year = self.entries["lnE_PublishedYear"].get()
        category = self.entries["lnE_Category"].get()
        price = self.entries["lnE_Quantity"].get()

        # Print the collected data (placeholder for actual functionality)
        print(f"Adding book: {book_name} by {author}")
        print(f"ISBN: {isbn}, Year: {pub_year}")
        print(f"Category: {category}, Price: {price}")

    #     # Here you would add code to save the book to a database or file

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = BookManagementAddBookApp(root)
    app.run()