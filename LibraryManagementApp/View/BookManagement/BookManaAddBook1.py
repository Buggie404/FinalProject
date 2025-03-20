from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


class BookManaAddBook1App:
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
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBookManaAddBook1")

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
        self.text_elements = {}
        self.buttons = {}

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()
        self.create_book_details()

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
        self.create_rounded_rectangle(289.0, 39.0, 875.0, 567.0, radius=10, color="#F1F1F1")

    # def create_background(self):
    #     """Create the main background elements"""
    #     # Sidebar background
    #     self.canvas.create_rectangle(
    #         0.0, 0.0, 262.0, 605.0,
    #         fill="#0A66C2", outline=""
    #     )
    #
    #     # Main panel background
    #     self.canvas.create_rectangle(
    #         289.0, 39.0, 875.0, 567.0,
    #         fill="#F0F0F0", outline=""
    #     )

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
        # Load title and icons
        self.load_image("image_2", (581.0, 69.0))
        self.load_image("image_3", (380.0, 132.0))
        self.load_image("image_4", (380.0, 200.0))
        self.load_image("image_5", (389.0, 268.0))
        self.load_image("image_8", (424.0, 336.0))
        self.load_image("image_6", (398.0, 404.0))
        self.load_image("image_7", (396.0, 472.0))
        self.load_image("image_9", (582.0, 533.0))

    def create_book_details(self):
        """Create the text elements displaying book information"""
        # Mới thêm
        """Create the text elements displaying book information"""
        # Default values
        isbn = self.book_data.get('book_id', '')
        title = self.book_data.get('title', '')
        author = self.book_data.get('author', '')
        published_year = self.book_data.get('published_year', '')
        category = self.book_data.get('category', '')
        quantity = self.book_data.get('quantity', '')

        # Book details
        self.lbl_ISBN = self.canvas.create_text(
            581.0, 119.0,
            anchor="nw",
            text="2005018",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_Title = self.canvas.create_text(
            581.0, 187.0,
            anchor="nw",
            text="Clara Callen",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_Author = self.canvas.create_text(
            581.0, 255.0,
            anchor="nw",
            text="Richard Bruce Wright",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_PublishedYear = self.canvas.create_text(
            581.0, 323.0,
            anchor="nw",
            text="2001",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_Category = self.canvas.create_text(
            581.0, 390.0,
            anchor="nw",
            text="Fantasy",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_Quantity = self.canvas.create_text(
            581.0, 459.0,
            anchor="nw",
            text="3",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

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

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")

        if button_name == "btn_AddBook" and self.controller:
            self.controller.navigate_to_add_book()

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = BookManaAddBook1App(root)
    app.run()