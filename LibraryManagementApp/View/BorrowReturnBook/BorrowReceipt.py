from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, Listbox

class BorrowReceiptApp:
    def __init__(self, root, assets_path=None):
        self.root = root
        self.root.geometry("898x605")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBorrowReceipt")
        
        self.images = {}
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
        
        self.load_images()
        self.create_main_layout()
        self.create_sidebar()
        self.create_main_content()
        self.create_buttons()
    
    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)
    
    def load_images(self):
        """Load all image assets"""
        image_files = [
            "image_1.png",
            "image_3.png",
            "btn_BackToHomepage.png",
            "btn_ReturnBook.png",
            "btn_BorrowBook.png",
            "btn_Back.png"
        ]
        
        for image_file in image_files:
            full_path = self.relative_to_assets(image_file)
            try:
                self.images[image_file] = PhotoImage(file=full_path)
            except Exception as e:
                print(f"Error loading image {full_path}: {e}")

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
    
    def create_main_layout(self):
        """Create the main layout rectangles"""
        # Main content area background
        self.create_rounded_rectangle(
            285.0,
            80.0,
            871.0,
            525.0,
            radius = 10,
            color="#F1F1F1"
        )
        
        # Receipt table
        # self.tbl_Receipt = self.canvas.create_rectangle(
        #     395.0,
        #     173.0,
        #     760.0,
        #     416.0,
        #     fill="#D9D9D9",
        #     outline=""
        # )

        """Cach 1"""
        # self.tbl_frame = ttk.Frame(self.root)
        # self.tbl_frame.place(x=395.0, y=193.0, width=365.0, height=224.0)

        # self.tbl_scroll = ttk.Scrollbar(self.tbl_frame, orient="horizontal")
        # self.tbl_scroll.pack(side="bottom", fill="x")

        # self.tbl_Receipt = ttk.Treeview(
        #     self.tbl_frame,
        #     columns = ("receipt_id", "user_id", "book_id", "borrowed_quantity", "borrow_date", "return_date"),
        #     show = "headings",
        #     style = "Treeview"
        # )

        # self.tbl_Receipt.column("receipt_id", width=60, anchor="center")
        # self.tbl_Receipt.column("user_id", width=60, anchor="center")
        # self.tbl_Receipt.column("book_id", width=100, anchor="center")
        # self.tbl_Receipt.column("borrowed_quantity", width=120, anchor="center")
        # self.tbl_Receipt.column("borrow_date", width=100, anchor="center")
        # self.tbl_Receipt.column("return_date", width=150, anchor="center")

        # self.tbl_Receipt.heading("receipt_id", text="Receipt ID")
        # self.tbl_Receipt.heading("user_id", text="ID")
        # self.tbl_Receipt.heading("book_id", text="ISBN")
        # self.tbl_Receipt.heading("borrowed_quantity", text="Borrowed Quantity")
        # self.tbl_Receipt.heading("borrow_date", text="Borrow Date")
        # self.tbl_Receipt.heading("return_date", text="Book Return Deadline")

        # self.tbl_Receipt.pack(fill="both", expand=True)

        # self.tbl_scroll.config(command=self.tbl_Receipt.xview)
        # self.tbl_Receipt.config(xscrollcommand=self.tbl_scroll.set)

        """Cach 2"""
        """Display receipt details in a row-like format using labels."""
        self.lbl_frame = ttk.Frame(self.root)
        self.lbl_frame.place(x=395, y=193, width=365, height=224)

        # Define Fields
        fields = ["Receipt ID:", "User ID:", "ISBN:", "Borrowed Quantity:", "Borrow Date:", "Return Deadline:"]
        
        # Create Labels for Each Field
        for i, field in enumerate(fields):
            label = ttk.Label(self.lbl_frame, text=field, font=("Arial", 12, "bold"))
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            # Placeholder Label (To Be Updated with Data Later)
            value_label = ttk.Label(self.lbl_frame, text="N/A", font=("Arial", 12))
            value_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        """Cach 3"""
        # """Display multiple receipts in a vertical format using Listbox."""
        # self.list_frame = ttk.Frame(self.root)
        # self.list_frame.place(x=395, y=193, width=365, height=224)

        # self.listbox = Listbox(self.list_frame, font=("Arial", 12), height=6, width=50)
        # self.listbox.pack(fill="both", expand=True)

        # # Example Data (You Can Fetch Real Data Later)
        # sample_data = [
        #     "Receipt ID: 213, User ID: 136, ISBN: 966986105",
        #     "Receipt ID: 214, User ID: 164, ISBN: 312953453",
        #     "Receipt ID: 215, User ID: 111, ISBN: 316973742"
        # ]

        # for item in sample_data:
        #     self.listbox.insert("end", item)

        """Cach 4"""
        # Create frame for the table
        # self.tbl_frame = ttk.Frame(self.root)
        # self.tbl_frame.place(x=395.0, y=193.0, width=365.0, height=224.0)

        # # Create vertical scrollbar
        # self.tbl_scroll_y = ttk.Scrollbar(self.tbl_frame, orient="vertical")
        # self.tbl_scroll_y.pack(side="right", fill="y")

        # # Create horizontal scrollbar
        # self.tbl_scroll_x = ttk.Scrollbar(self.tbl_frame, orient="horizontal")
        # self.tbl_scroll_x.pack(side="bottom", fill="x")

        # # Define row headers (these will be displayed in the leftmost column)
        # self.row_headers = [
        #     "Receipt ID", 
        #     "ID", 
        #     "ISBN", 
        #     "Borrowed Quantity", 
        #     "Borrow Date", 
        #     "Book Return Deadline"
        # ]

        # # Create the Treeview with show="tree" to hide column headers
        # self.tbl_Receipt = ttk.Treeview(
        #     self.tbl_frame,
        #     show="tree",  # Only show tree structure, no column headers
        #     style="Treeview"
        # )
        # self.tbl_Receipt.pack(fill="both", expand=True)

        # # Configure columns for data (we'll add 3 data columns as an example)
        # num_data_columns = 3  # Adjust based on how many records you want to display at once
        # self.tbl_Receipt["columns"] = tuple(f"col{i}" for i in range(num_data_columns))

        # # Configure the row header column width and other properties
        # self.tbl_Receipt.column("#0", width=150, minwidth=150, stretch=False)

        # # Configure data columns
        # for i in range(num_data_columns):
        #     self.tbl_Receipt.column(f"col{i}", width=100, minwidth=80, anchor="center", stretch=True)

        # # Insert rows (what would normally be column headers)
        # for header in self.row_headers:
        #     self.tbl_Receipt.insert("", "end", text=header, values=("", "", ""))

        # # Configure scrollbars
        # self.tbl_scroll_x.config(command=self.tbl_Receipt.xview)
        # self.tbl_scroll_y.config(command=self.tbl_Receipt.yview)
        # self.tbl_Receipt.config(xscrollcommand=self.tbl_scroll_x.set, yscrollcommand=self.tbl_scroll_y.set)

        # # Method to load data (call this when you have data to display)
        # def load_data(self, data_records):
        #     """
        #     Load data into the transposed table
        #     data_records: A list of receipt records (each record is a dictionary or tuple)
        #     """
        #     # Clear existing items first
        #     for item in self.tbl_Receipt.get_children():
        #         self.tbl_Receipt.delete(item)
            
        #     # Insert rows with data
        #     for i, header in enumerate(self.row_headers):
        #         # Extract the appropriate field from each record
        #         values = []
        #         for record in data_records:
        #             # Get the value corresponding to this row's field
        #             # Assuming record is a dictionary or an object with indexed access
        #             if isinstance(record, dict):
        #                 field_name = ["receipt_id", "user_id", "book_id", "borrowed_quantity", "borrow_date", "return_date"][i]
        #                 values.append(record.get(field_name, ""))
        #             else:  # If it's a tuple or list
        #                 values.append(record[i] if i < len(record) else "")
                
        #         # Insert the row with its values
        #         self.tbl_Receipt.insert("", "end", text=header, values=tuple(values))

    def create_sidebar(self):
        """Create the sidebar with buttons and logo"""
        # Blue sidebar background
        self.canvas.create_rectangle(
            0.0,
            0.0,
            262.0,
            605.0,
            fill="#0A66C2",
            outline=""
        )
        
        # Logo image
        if "image_3.png" in self.images:
            self.canvas.create_image(
                130.0,
                73.0,
                image=self.images["image_3.png"]
            )
        
        self.create_button("btn_BorrowBook.png", 0.0, 181.0, 262.0, 25.0, self.on_borrow_book_click)
        self.create_button("btn_ReturnBook.png", 0.0, 219.0, 262.0, 25.0, self.on_return_book_click)
        self.create_button("btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_click)
    
    def create_main_content(self):
        """Create the main content area"""
        # Header image
        if "image_1.png" in self.images:
            self.canvas.create_image(
                578.0,
                118.0,
                image=self.images["image_1.png"]
            )
    
    def create_buttons(self):
        """Create action buttons"""
        self.create_button("btn_Back.png", 421.0, 456.0, 313.0, 48.0, self.on_back_click)
    
    def create_button(self, image_name, x, y, width, height, command):
        """Helper method to create buttons"""
        if image_name not in self.images:
            print(f"Warning: Image {image_name} not found")
            return None
            
        button = Button(
            image=self.images[image_name], 
            borderwidth=0, 
            highlightthickness=0, 
            command=command, 
            relief="flat"
        )
        
        button.place(x=x, y=y, width=width, height=height)
        
        button_name = image_name.replace(".png", "")
        if button_name.startswith("btn_"):
            setattr(self, button_name, button)
            
        return button
    
    # Event handlers
    def on_borrow_book_click(self):
        print("btn_BorrowBook clicked")
        # Implement borrow book functionality here
    
    def on_return_book_click(self):
        print("btn_ReturnBook clicked")
        # Implement return book functionality here
    
    def on_back_to_homepage_click(self):
        print("btn_BackToHomepage clicked")
        # Implement back to homepage functionality here
    
    def on_back_click(self):
        print("btn_Back clicked")
        # Implement back button functionality here

# Entry point
if __name__ == "__main__":
    window = Tk()
    app = BorrowReceiptApp(window)
    window.mainloop()