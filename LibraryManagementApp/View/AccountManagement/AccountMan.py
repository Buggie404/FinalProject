# This file was restructured from the original Tkinter Designer output by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage


class ProfileApp:
    def __init__(self, root,assets_path=None):
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
            # Fix path - remove the "dcmTvT/" from the beginning
            self.assets_path = self.output_path / Path(r"build/assets/frameAccountManagement")


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

    # def create_background(self):
    #     """Create the main background elements"""
    #     # Left sidebar background
    #     self.canvas.create_rectangle(
    #         0.0, 0.0, 262.0, 605.0,
    #         fill="#0A66C2", outline=""
    #     )
    #
    #     # Main content areas
    #     self.canvas.create_rectangle(
    #         285.0, 257.0, 871.0, 560.0,
    #         fill="#F0F0F0", outline=""
    #     )
    #
    #     self.canvas.create_rectangle(
    #         285.0, 56.0, 871.0, 201.0,
    #         fill="#F0F0F0", outline=""
    #     )

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

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")


if __name__ == "__main__":
    window = Tk()
    app = ProfileApp(window)
    window.mainloop()