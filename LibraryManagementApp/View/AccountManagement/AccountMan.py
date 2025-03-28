# Import Lib
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import os
import sys

# Import base file path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, "View"))
sys.path.append(base_dir)

class AccountManagement:
    def __init__(self, root, user_data=None, assets_path=None, role=None):
        # Initialize the main window
        self.root = root
        self.user_data = user_data or []
        self.role=role
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        if self.user_data and len(self.user_data) > 6 and self.user_data[6] == "Admin":
            self.role = "admin"
        else:
            self.role = role or "user"

        self.output_path = Path(__file__).parent
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameAccountManagement")

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

        # Build UI components
        self.create_mainframe()
        self.create_sidebar()
        self.create_content_areas()
        self.create_profile_info()

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

    def create_mainframe(self):
        """Tạo nền chính với bo góc"""
        # Sidebar (không cần bo góc)
        self.canvas.create_rectangle(
            0.0, 0.0, 262.0, 605.0,
            fill="#0A66C2", outline=""
        )

        # Hình chữ nhật lớn nằm ngang (bo góc)
        self.create_rounded_rectangle(285.0, 257.0, 871.0, 560.0, radius=10, color="#F1F1F1")
        self.create_rounded_rectangle(285.0, 56.0, 871.0, 201.0, radius=10, color="#F1F1F1")

    def load_image(self, image_name, position):
        """Load an image and place it on the canvas"""
        file_path = self.relative_to_assets(f"{image_name}.png")

        if not os.path.exists(file_path):
            return

        # Nếu file tồn tại, load vào chương trình
        self.images[image_name] = PhotoImage(file=file_path)

        self.canvas.create_image(
            position[0], position[1],
            image=self.images[image_name]
        )

    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Logo
        self.load_image("image_1", (131.0, 74.0))

        # Sidebar buttons
        self.create_button("btn_ChangePassword", (0.0, 181.0, 261.0, 25.0))
        self.create_button("btn_EditAccountInformation", (0.0, 219.0, 261.0, 25.0))
        self.create_button("btn_SignOut", (0.0, 257.0, 261.0, 25.0))
        self.create_button("btn_BacktoHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_content_areas(self):
        """Create the profile content areas with images"""
        # Profile section images
        self.load_image("image_9", (358.0, 125.0))
        self.load_image("image_4", (464.0, 125.0))
        self.load_image("image_5", (479.0, 84.0))
        self.load_image("image_6", (472.0, 166.0))

        # Details section images
        self.load_image("image_8", (578.0, 288.0))
        self.load_image("image_2", (355.0, 348.0))
        self.load_image("image_7", (372.0, 425.0))
        self.load_image("image_3", (365.0, 505.0))

    def create_profile_info(self):
        """Create the text elements displaying user information"""
        # User profile info
        self.lbl_Name = self.canvas.create_text(
            540.0, 71.0,
            anchor="nw",
            text="Nguyen Van B",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_ID = self.canvas.create_text(
            540.0, 113.0,
            anchor="nw",
            text="0900900",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_Role = self.canvas.create_text(
            540.0, 153.0,
            anchor="nw",
            text="Admin",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        # User details
        self.lbl_Username = self.canvas.create_text(
            505.0, 336.0,
            anchor="nw",
            text="adbc18",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_EmailAddress = self.canvas.create_text(
            505.0, 410.0,
            anchor="nw",
            text="abc@gmail.com",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        self.lbl_DateOfBirth = self.canvas.create_text(
            505.0, 492.0,
            anchor="nw",
            text="08/09/2005",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )

        if self.user_data:
            self.update_profile_info()
        
    def update_profile_info(self):
        """Update profile information with actual user data"""
        if self.user_data:
            # Update user profile info
            self.canvas.itemconfig(self.lbl_Name, text=self.user_data[1])  # name
            self.canvas.itemconfig(self.lbl_ID, text=self.user_data[0])  # user_id
            self.canvas.itemconfig(self.lbl_Role, text=self.user_data[6])  # role
            
            # Update user details
            self.canvas.itemconfig(self.lbl_Username, text=self.user_data[2])  # username
            self.canvas.itemconfig(self.lbl_EmailAddress, text=self.user_data[3])  # email
            self.canvas.itemconfig(self.lbl_DateOfBirth, text=self.user_data[5])  # date_of_birth

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

    def button_click(self, button_name):
        """Handle button click events"""

        if button_name == "btn_ChangePassword":
            self.root.destroy()
            from AccountManagement.AccountChangePassword import AccountChangePwApp
            changepass_root = Tk()
            changepass = AccountChangePwApp(changepass_root, user_data=self.user_data)
            changepass_root.mainloop()

        elif button_name == "btn_EditAccountInformation":
            self.root.destroy()
            from AccountManagement.AccountEditInfo import AccountEditInfoApp
            editinfo_root = Tk()
            editinfo = AccountEditInfoApp(editinfo_root, user_data=self.user_data)
            editinfo_root.mainloop()

        elif button_name == "btn_SignOut":
            from noti_tab_view_1 import Sign_Out
            Sign_Out(self.root)

        else:
            self.root.destroy()
            from Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role=self.role, user_data=self.user_data)
            homepage_root.mainloop()



if __name__ == "__main__":
    window = Tk()
    app = AccountManagement(window)
    window.mainloop()