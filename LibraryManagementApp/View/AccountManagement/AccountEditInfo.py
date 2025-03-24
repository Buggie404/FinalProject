# Import Lib
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os
import sys

class AccountEditInfoApp: # Chưa có hàm để xử lý input của lineEdit (lấy input của lnE) -> thêm để bên Controller xử lý tiếp phần này nha
    def __init__(self, root, user_data=None, user_id = None, assets_path=None, role=None):
        # Initialize the main window
        self.root = root
        self.user_data=user_data
        self.role=role
        # self.user_id = user_id
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        if self.user_data and len(self.user_data) > 6 and self.user_data[6] == "Admin":
            self.role = "admin"
        else:
            self.role = role or "user"

        # Import Model to take user data
        # from Model.user_model import User
        # self.user_data = User.get_id(self.user_id)

        # import controller that hndel Edit Account Information
        from Controller.account_management_controller import AccountEditInfoController 
        self.controller = AccountEditInfoController(user_data)

        # Set up asset paths
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameAccountEditInfo")

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
        self.prefill_user_data()

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
        self.load_image("image_4", (131.0, 74.0))

        # Create sidebar buttons
        self.create_button("btn_ChangePassword", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditAccountInformation", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        """Create the main panel with form elements"""
        # Title image
        self.load_image("image_1", (577.0, 120.0))

        # Create form entries with icons
        self.create_entry_with_icon("lnE_NewUsername", "image_2", (542.0, 199.0, 273.0, 46.0), (678.5, 223.0), (381.0, 223.0))
        self.create_entry_with_icon("lnE_NewDateOfBirth", "image_3", (542.0, 277.0, 273.0, 46.0), (678.5, 301.0), (375.0, 301.0))

        # Create submit button
        self.create_button("btn_Apply", (421.0, 448.0, 313.0, 48.0))

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

    def prefill_user_data(self):
        """Prefill user data in the form entries with current data"""
        if self.user_data:
            # Prefill username
            if self.user_data[2]:  # Username is at index 2
                self.entries["lnE_NewUsername"].delete(0, 'end')
                self.entries["lnE_NewUsername"].insert(0, self.user_data[2])
            
            # Prefill date of birth
            if self.user_data[5]:  # Date of birth is at index 5
                self.entries["lnE_NewDateOfBirth"].delete(0, 'end')
                self.entries["lnE_NewDateOfBirth"].insert(0, self.user_data[5])

    def create_entry_with_icon(self, entry_name, icon_name, entry_dimensions, bg_position, icon_position):
        """Create an entry field with background and icon"""
        # Create entry background
        self.images[entry_name] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )
        self.canvas.create_image(
            bg_position[0], bg_position[1],
            image=self.images[entry_name]
        )

        # Create entry field
        entry = Entry(
            bd=0,
            bg="#E7DCDC",
            fg="#000716",
            highlightthickness=0
        )
        entry.place(
            x=entry_dimensions[0],
            y=entry_dimensions[1],
            width=entry_dimensions[2],
            height=entry_dimensions[3]
        )
        self.entries[entry_name] = entry

        # Load and place icon
        self.load_image(icon_name, icon_position)

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")
        if button_name == "btn_EditAccountInformation": # switch back to Account Mainwindow
            self.root.destroy()
            from View.AccountManagement.AccountMan import AccountManagement
            account_root = Tk()
            account = AccountManagement(account_root, user_data=self.user_data)
            account.root.mainloop()
        elif button_name == "btn_ChangePassword": # switch to Change Password window
            self.root.destroy()
            from View.AccountManagement.AccountChangePassword import AccountChangePwApp
            changepass_root = Tk()
            changepass = AccountChangePwApp(changepass_root, user_data=self.user_data)
            changepass.root.mainloop()
        elif button_name == "btn_BackToHomepage": # switch back to Homepage
            self.root.destroy()
            from View.Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role=self.role, user_data=self.user_data)
            homepage.root.mainloop()
        else: # For btn_Apply
            self.controller.handle_apply_click(self)

    def run(self): 
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = AccountEditInfoApp(root)
    app.run()