from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


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
        self.buttons = {}

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
        self.create_rounded_rectangle(285.0, 47.0, 871.0, 558.0, radius=10, color="#F1F1F1")

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
        self.load_image("image_2", (577.0, 70.0))
        self.load_image("image_3", (336.0, 135.0))
        self.load_image("image_4", (345.0, 212.0))
        self.load_image("image_7", (380.0, 289.0))
        self.load_image("image_5", (354.0, 366.0))
        self.load_image("image_6", (352.0, 443.0))

        # Create save button
        self.create_button("btn_Confirm", (421.0, 498.0, 313.0, 48.0))

    def create_entry_fields(self):
        """Create the entry fields for book information"""
        # First Entry (Title)
        self.create_entry_field("lnE_Title", (679.5, 136.0), (543.0, 112.0, 273.0, 46.0))

        # Second Entry (Author)
        self.create_entry_field("lnE_Author", (679.5, 213.0), (543.0, 189.0, 273.0, 46.0))

        # Third Entry (PublishedYear)
        self.create_entry_field("lnE_PublishedYear", (679.5, 290.0), (543.0, 266.0, 273.0, 46.0))

        # Fourth Entry (Category)
        self.create_entry_field("lnE_Category", (679.5, 367.0), (543.0, 343.0, 273.0, 46.0))

        # Fifth Entry (Quantity)
        self.create_entry_field("lnE_Quantity", (679.5, 444.0), (543.0, 420.0, 273.0, 46.0))

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

        # Store button widget in dictionary
        self.buttons[button_name] = button

    def create_entry_field(self, entry_name, bg_position, dimensions):
        """Create an entry field with background image"""
        # Create entry background image
        self.images[f"{entry_name}_bg"] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )
        self.canvas.create_image(
            bg_position[0],
            bg_position[1],
            image=self.images[f"{entry_name}_bg"]
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
    app = BookManagementApp(window)
    app.run()