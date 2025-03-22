# Import Lib
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os
import sys

# Import base file path 
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, "View"))
sys.path.append(base_dir)

class AccountEditInfo2App:
    def __init__(self, root, user_id=None, user_data=None, assets_path=None):
        # Initialize the main window
        self.root = root
        self.user_id = user_id
        self.user_data = user_data
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        # Import Model to fetch user_data for account tracking
        from Model.user_model import User
        user_data = User.get_id(self.user_id)

        # Set up asset paths
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameAccountEditInfo2")

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

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()

    def relative_to_assets(self, path):
        """Helper function to get the absolute path to assets"""
        return self.assets_path / Path(path)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, color):
        """Vẽ hình chữ nhật có bo góc"""
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
        """Create the background elements with rounded corners for the main panel"""
        # Sidebar (không cần bo góc)
        self.canvas.create_rectangle(
            0.0, 0.0, 262.0, 605.0,
            fill="#0A66C2", outline=""
        )

        # Hình chữ nhật lớn nằm ngang (bo góc)
        self.create_rounded_rectangle(285.0, 80.0, 871.0, 525.0, radius=10, color="#F0F0F0")

    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Load and place logo
        self.load_image("image_1", (131.0, 74.0))

        # Create sidebar buttons
        self.create_button("btn_ChangePassword", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditAccountInformation", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        """Create the main panel elements"""
        # Title image
        self.load_image("image_2", (578.0, 130.0))

        # Additional image
        self.load_image("image_3", (578.0, 251.0))

        # Create buttons in the main panel
        self.create_button("btn_Redo", (421.0, 360.0, 313.0, 48.0))
        self.create_button("btn_Return", (421.0, 448.0, 313.0, 48.0))

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
        print(f"{button_name} clicked")
        if button_name == "btn_EditAccountInformation" or button_name == "btn_Redo": # If clicked edit information in success/failed window -> go back to first AccountChangePass
            self.root.destroy()
            from AccountEditInfo import AccountEditInfoApp
            changepass_root = Tk()
            changeoass = AccountEditInfoApp(changepass_root, user_id = self.user_id)
            changepass_root.mainloop()
        elif button_name == "btn_Return": # Return to Account MainWindow
            self.root.destroy()
            from AccountMan import AccountManagement
            account_root = Tk()
            account = AccountManagement(account_root, user_data = self.user_data)
            account_root.mainloop()
        elif button_name == "btn_BackToHomepage":
            self.root.destroy()
            from Homepage import HomepageApp
            role = 'admin' if self.user_data[6] == "Admin" else "User"
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role = role, user_data = self.user_data)
            homepage_root.mainloop()
        else: # If clicked edit account information here, nothing happends
            pass

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = AccountEditInfo2App(root)
    app.run()