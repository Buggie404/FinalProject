from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


class UserEditAccountApp:
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
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameUserEditAccount1")

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
        self.create_user_details()

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
        self.create_rounded_rectangle(285.0, 80.0, 871.0, 525.0, radius=10, color="#F1F1F1")

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
        # Load header image and user icon
        self.load_image("image_6", (578.0, 122.0))

        # Load field icons
        self.load_image("image_3", (375.0, 197.0))  # ID icon
        self.load_image("image_2", (391.0, 258.0))  # Name icon
        self.load_image("image_5", (429.0, 322.0))  # Email icon
        self.load_image("image_4", (412.0, 386.0))  # Username icon

        # Create update button
        self.create_button("btn_ResetPassword", (421.0, 443.0, 313.0, 48.0))

    def create_user_details(self):
        """Create the text elements displaying user information"""
        # User details
        self.lbl_ID = self.canvas.create_text(
            598.0, 185.0,
            anchor="nw",
            text="123456789",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_Name = self.canvas.create_text(
            598.0, 249.0,
            anchor="nw",
            text="Bichnhi89",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_EmailAddress = self.canvas.create_text(
            598.0, 313.0,
            anchor="nw",
            text="bnhi@.com",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_Username = self.canvas.create_text(
            598.0, 377.0,
            anchor="nw",
            text="fghjkkm",
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

    def create_entry(self, entry_name, dimensions, bg_color="#FFFFFF"):
        """Create an entry field with the given parameters"""
        entry = Entry(
            self.root,
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

        # Specific button actions can be added here
        if button_name == "button_4":
            self.update_user_info()
        elif button_name == "button_1":
            self.go_back_to_homepage()

    def update_user_info(self):
        """Handle updating the user information"""
        print("Updating user information...")
        # Code to update user information in a database would go here

    def go_back_to_homepage(self):
        """Navigate back to homepage"""
        print("Navigating back to homepage...")
        # Code to navigate back to homepage would go here

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = UserEditAccountApp(root)
    app.run()