from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


class BookEdit1App:
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
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBookManaEditBook1")

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

        # Store images as instance variables to prevent garbage collection
        self.images = {}
        self.entries = {}

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()
        self.create_entry_fields()

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
        self.create_rounded_rectangle(291.0, 39.0, 877.0, 567.0, radius=10, color="#F1F1F1")

    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Logo
        self.load_image("image_1", (131.0, 74.0))

        # Sidebar buttons
        self.create_button("btn_AddBook", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditBookInformation", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        """Create the main panel elements"""
        # Load title and icons
        self.load_image("image_2", (583.0, 69.0))
        self.load_image("image_3", (337.0, 124.0))
        self.load_image("image_4", (337.0, 192.0))
        self.load_image("image_5", (346.0, 260.0))
        self.load_image("image_8", (381.0, 328.0))
        self.load_image("image_6", (355.0, 396.0))
        self.load_image("image_7", (353.0, 464.0))

        # Create save button
        self.create_button("btn_Confirm", (425.0, 508.0, 313.0, 48.0))

    def create_entry_fields(self):
        """Create the entry fields for book information"""
        # ISBN Entry
        self.create_entry_field("lnE_ISBN", (681.5, 124.0), (545.0, 100.0, 273.0, 46.0))

        # Title Entry
        self.create_entry_field("lnE_Title", (681.5, 192.0), (545.0, 168.0, 273.0, 46.0))

        # Author Entry
        self.create_entry_field("lnE_Author", (681.5, 260.0), (545.0, 236.0, 273.0, 46.0))

        # Year Entry
        self.create_entry_field("lnE_PublishedYear", (681.5, 328.0), (545.0, 304.0, 273.0, 46.0))

        # Category Entry
        self.create_entry_field("lnE_Category", (681.5, 396.0), (545.0, 372.0, 273.0, 46.0))

        # Quantity Entry
        self.create_entry_field("lnE_Quantity", (681.5, 464.0), (545.0, 440.0, 273.0, 46.0))

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

    def create_entry_field(self, entry_name, bg_position, dimensions):
        """Create an entry field with background image"""
        # Create entry background image
        self.images[entry_name] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )
        self.canvas.create_image(
            bg_position[0],
            bg_position[1],
            image=self.images[entry_name]
        )

        # Create entry widget
        entry = Entry(
            bd=0,
            bg="#E7DCDC",
            fg="#000716",
            highlightthickness=0
        )
        entry.place(
            x=dimensions[0],
            y=dimensions[1],
            width=dimensions[2],
            height=dimensions[3]
        )

        # Store entry widget in dictionary
        self.entries[entry_name] = entry

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    window = Tk()
    app = BookEdit1App(window)
    app.run()