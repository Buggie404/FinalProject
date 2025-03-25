from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
import os
import sys
from Homepage import HomepageApp 


class LogInApp:
    def __init__(self, root, assets_path=None):
        self.root = root
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.output_path = Path(__file__).parent
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path / Path(r"Ultilities/build/assets/frameLogIn")
        
        # Store image references to prevent garbage collection
        self.images = {}
        
        # Setup UI components
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

        # Load all images
        self.load_images()
        
        # Create UI elements
        self.create_sidebar()
        self.create_main_content()
        self.create_login_button()
    
    def relative_to_assets(self, path: str) -> Path:
        """Convert relative asset path to absolute path"""
        return self.assets_path / Path(path)
    
    def load_images(self):
        """Load all required images"""
        image_files = [
            "lnE_Email.png", 
            "lnE_Password.png", 
            "btn_LogIn.png", 
            "image_1.png", 
            "image_2.png"
        ]
        
        for image_file in image_files:
            full_path = self.relative_to_assets(image_file)
            try:
                self.images[image_file] = PhotoImage(file=full_path)
            except Exception as e:
                pass
    
    def create_sidebar(self):
        """Create the blue sidebar rectangle and its content"""
        self.canvas.create_rectangle(
            0.0,
            0.0,
            299.0,
            605.0,
            fill="#0A66C2",
            outline=""
        )
        
        # Add Logo
        if "image_1.png" in self.images:
            self.canvas.create_image(
                149.0,
                250.0,
                image=self.images["image_1.png"]
            )
    
    def create_main_content(self):
        """Create the main content area with entry fields and header image"""
        # Create header image
        if "image_2.png" in self.images:
            self.canvas.create_image(
                606.0,
                147.0,
                image=self.images["image_2.png"]
            )
        
        # Create email entry
        self.create_entry(
            "lnE_Email.png", 
            600.5, 
            317.0, 
            464.0, 
            293.0, 
            273.0, 
            46.0
        )
        
        # Create password entry
        self.create_entry(
            "lnE_Password.png", 
            600.5, 
            404.0, 
            464.0, 
            380.0, 
            273.0, 
            46.0
        )

    def create_entry(self, image_name, img_x, img_y, entry_x, entry_y, width, height, placeholder=None):
        """Helper method to create an entry field with background image and placeholder text"""
        # Display the background image
        if image_name in self.images:
            self.canvas.create_image(
                img_x,
                img_y,
                image=self.images[image_name]
            )
        
        # Determine if this is a password field and set appropriate placeholder
        is_password = "Password" in image_name
        if placeholder is None:
            if "Email" in image_name:
                placeholder = "Email"
            elif "Password" in image_name:
                placeholder = "Password"
            else:
                placeholder = ""
    
        # Create the entry widget
        entry = Entry(
            bd=0,
            bg="#E8DCDC",
            fg="grey",  # Start with grey text for placeholder
            highlightthickness=0
        )
        
        # Position the entry
        entry.place(
            x=entry_x,
            y=entry_y,
            width=width,
            height=height
        )
        
        # Set initial placeholder text
        entry.insert(0, placeholder)
        
        # Store the entry's properties in the widget itself for easy access in callbacks
        entry.is_password = is_password
        entry.placeholder = placeholder
        entry.has_content = False
        
        # Setup focus events to handle placeholder behavior
        entry.bind("<FocusIn>", self._on_entry_focus_in)
        entry.bind("<FocusOut>", self._on_entry_focus_out)
        
        # For password field, we need to track when the content changes
        if is_password:
            entry.bind("<KeyRelease>", self._on_entry_key_event)
        
        # Store reference to entry fields for later access
        if image_name == "lnE_Email.png":
            self.lnE_Email = entry
        elif image_name == "lnE_Password.png":
            self.lnE_Password = entry
                
        return entry

    def _on_entry_focus_in(self, event):
        """Remove placeholder text when entry gets focus"""
        entry = event.widget
        if entry.get() == entry.placeholder:
            entry.delete(0, "end")
            entry.config(fg="#000716")  # Change to normal text color
            # Set show attribute for password fields
            if entry.is_password:
                entry.config(show="•")

    def _on_entry_focus_out(self, event):
        """Add placeholder text if entry is empty and loses focus"""
        entry = event.widget
        if entry.get() == "":
            entry.insert(0, entry.placeholder)
            entry.config(fg="grey", show="")  # Grey text, no bullets for placeholder
            entry.has_content = False
        else:
            entry.has_content = True

    def _on_entry_key_event(self, event):
        """Track when password field has content and apply bullet mask"""
        entry = event.widget
        if entry.is_password:
            # If have any content and it's not just the placeholder, show bullets
            if entry.get() != "" and entry.get() != entry.placeholder:
                entry.config(show="•")
                entry.has_content = True
            # If field is empty but still has focus, keep show="•" but mark as empty
            elif entry.get() == "":
                entry.has_content = False
    
    def create_login_button(self):
        """Create the login button"""
        if "btn_LogIn.png" in self.images:
            self.create_button(
                "btn_LogIn.png",
                444.0,
                467.0,
                313.0,
                48.0,
                self.on_login_clicked
            )
    
    def create_button(self, image_name, x, y, width, height, command):
        """Helper method to create a button"""
        button = Button(
            image=self.images[image_name],
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        
        button.place(
            x=x,
            y=y,
            width=width,
            height=height
        )
        
        # Store reference to login button
        if image_name == "btn_LogIn.png":
            self.btn_LogIn = button
            
        return button
    
    def on_login_clicked(self):
        """Handle login button click event"""
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(parent_dir)
        from Controller.auth_controller import Authen
        email = self.lnE_Email.get()
        password = self.lnE_Password.get()

        success, user_data = Authen.check_account_login(email, password)

        if success:  # if account is valid -> cho chuyển sang Homepage
            self.root.destroy()
            role = Authen.check_account_role(email)
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role=role, user_data=user_data)
            homepage_root.mainloop()
        else:  # else -> cho hiện Invalid(self.root, 'account')
            from noti_tab_view_1 import Invalid
            Invalid(self.root, 'account')



if __name__ == "__main__":
    window = Tk()
    app = LogInApp(window)
    window.mainloop()