from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage


class AccountManagementApp:
    def __init__(self, root, assets_path=None):
        # Initialize the main window
        self.root = root
        self.root.geometry("898x605")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        # Set up asset paths
        self.output_path = Path(__file__).parent
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path / Path(r"build/assets/frameAccountChangePw")

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
        self.create_mainframe()
        self.create_sidebar()
        self.create_main_panel()

    def relative_to_assets(self, path):
        return self.assets_path / Path(path)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, color):
        self.canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, fill=color, outline=color)
        self.canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, fill=color, outline=color)
        self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill=color, outline=color)
        self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill=color, outline=color)
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)

    def create_mainframe(self):
        self.canvas.create_rectangle(0.0, 0.0, 262.0, 605.0, fill="#0A66C2", outline="")
        self.create_rounded_rectangle(285.0, 80.0, 871.0, 525.0, radius=10, color="#F1F1F1")

    def create_sidebar(self):
        self.load_image("image_5", (131.0, 74.0))
        self.create_button("btn_ChangePassword", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditAccountInformation", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        self.load_image("image_1", (577.0, 120.0))
        self.create_entry_with_icon("lnE_CurrentPassword", "image_2", (544.0, 181.0, 273.0, 46.0), (680.5, 205.0), (409.0, 204.0))
        self.create_entry_with_icon("lnE_NewPassword", "image_3", (544.0, 267.0, 273.0, 46.0), (680.5, 291.0), (392.0, 291.0))
        self.create_entry_with_icon("lnE_ChangePassword", "image_4", (544.0, 355.0, 273.0, 46.0), (680.5, 379.0), (402.0, 379.0))
        self.create_button("btn_ChangePasswordConfirm", (421.0, 448.0, 313.0, 48.0))

    def load_image(self, image_name, position):
        self.images[image_name] = PhotoImage(file=self.relative_to_assets(f"{image_name}.png"))
        self.canvas.create_image(position[0], position[1], image=self.images[image_name])

    def create_button(self, button_name, dimensions):
        self.images[button_name] = PhotoImage(file=self.relative_to_assets(f"{button_name}.png"))
        button = Button(image=self.images[button_name], borderwidth=0, highlightthickness=0, command=lambda: self.button_click(button_name), relief="flat")
        button.place(x=dimensions[0], y=dimensions[1], width=dimensions[2], height=dimensions[3])
        self.buttons[button_name] = button

    def create_entry_with_icon(self, entry_name, icon_name, entry_dimensions, bg_position, icon_position):
        self.images[entry_name] = PhotoImage(file=self.relative_to_assets(f"{entry_name}.png"))
        self.canvas.create_image(bg_position[0], bg_position[1], image=self.images[entry_name])
        entry = Entry(bd=0, bg="#E7DCDC", fg="#000716", highlightthickness=0, show="•")
        entry.place(x=entry_dimensions[0], y=entry_dimensions[1], width=entry_dimensions[2], height=entry_dimensions[3])
        self.entries[entry_name] = entry
        self.load_image(icon_name, icon_position)

    def button_click(self, button_name):
        print(f"{button_name} clicked")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = AccountManagementApp(root)
    app.run()
