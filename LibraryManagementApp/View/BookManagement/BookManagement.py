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

        # Main content panel
        self.tbl_Book = self.canvas.create_rectangle(
            285.0, 156.0, 871.0, 542.0,
            fill="#D9D9D9", outline=""
        )

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
        self.create_button("btn_DeleteAccount", (719.0, 552.0, 115.0, 43.0))

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

    # def create_entry(self, entry_name, image_position, dimensions, bg_color):
    #     """Create an entry field with the given parameters"""
    #     self.images[entry_name] = PhotoImage(
    #         file=self.relative_to_assets(f"{entry_name}.png")
    #     )
    #
    #     entry_bg = self.canvas.create_image(
    #         image_position[0],
    #         image_position[1],
    #         image=self.images[entry_name]
    #     )
    #
    #     entry = Entry(
    #         bd=0,
    #         bg=bg_color,
    #         fg="#000716",
    #         highlightthickness=0
    #     )
    #
    #     entry.place(
    #         x=dimensions[0],
    #         y=dimensions[1],
    #         width=dimensions[2],
    #         height=dimensions[3]
    #     )
    #
    #     self.entries[entry_name] = entry

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = BookManagementApp(root)
    app.run()