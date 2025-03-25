from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


class UserEditAccountApp:
    def __init__(self, root, user_data = None, role = None, assets_path=None):
        # Initialize the main window
        self.root = root
        self.role = role
        self.user_data = user_data

        # Store these directly on the root window so the controller can access them
        self.root.role = role
        self.root.user_data = user_data

        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        # Only determine role if not explicitly provided
        if self.role is None:
            if self.user_data and len(self.user_data) > 6 and self.user_data[6] == "Admin":
                self.role = "admin"
            else:
                self.role = "user"

        self.output_path = Path(__file__).parent
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameUserEditAccount")

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
        self.load_image("image_1", (130.0, 74.0))

        # Create sidebar buttons
        self.create_button("btn_AddAccount", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditAccountPassword", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        """Create the main panel elements"""
        # Load header image
        self.load_image("image_3", (578.0, 84.0))

        # Load user icon
        self.load_image("image_2", (456.0, 139.0))

        # Create password entry field
        self.create_entry("lnE_InputID", (678.5, 140.5), (549.5, 124.0, 258.0, 31.0), "#D9D9D9")

        # Create update button
        self.create_button("btn_Search", (421.0, 181.0, 313.0, 48.0))

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

    def button_click(self, button_name):
        """Handle button click events"""
        if button_name == "btn_AddAccount": # Switch to Add Account
            self.root.destroy()
            from View.UserManagement.UserAddAccount import UserAddAccountApp
            add_root = Tk()
            add = UserAddAccountApp(add_root, user_data=self.user_data, role=self.role)
            add_root.mainloop()

        elif button_name == "btn_EditAccountPassword":
            # Switch back to User Management
            self.root.destroy()
            from View.UserManagement.UserManagement import UserManagementApp
            user_root = Tk()
            user = UserManagementApp(user_root, user_data=self.user_data)
            user_root.mainloop()

        elif button_name == "btn_BackToHomepage":
            # Switch to Homepage
            self.root.destroy()
            from View.Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role=self.role, user_data=self.user_data)
            homepage_root.mainloop()

        elif button_name == "btn_Search":
            # Get user ID from input field
            user_id = self.entries["lnE_InputID"].get().strip()
            
            # Create controller instance
            from Controller.user_controller import ResetPasswordController
            controller = ResetPasswordController()
            
            # The controller will handle validation and notifications
            controller.switch_to_user_edit_account1(self.root, user_id)

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = UserEditAccountApp(root)
    app.run()