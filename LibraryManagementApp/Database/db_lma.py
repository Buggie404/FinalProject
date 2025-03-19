# import sqlite3

# class Database:
#     def __init__(self):
#         self.conn = sqlite3.connect('LibraryManagementApp/Database/library.db')
#         self.cursor = self.conn.cursor()

#     def close(self):
#         self.conn.close()

import sqlite3
import os

class Database:
    def __init__(self):
        # Thử nhiều cách tìm đường dẫn đến file database
        db_paths = []
        
        # Xác định thư mục hiện tại
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_paths.append(os.path.join(os.path.dirname(os.path.dirname(current_dir)), "LibraryManagementApp", "Database", "library.db"))
        self.conn = None
        self.cursor = None
        
        for path in db_paths:
            if os.path.exists(path):
                try:
                    self.conn = sqlite3.connect(path)
                    self.cursor = self.conn.cursor()
                    print(f"✅ Kết nối database thành công: {path}")
                    break
                except sqlite3.Error as e:
                    print(f"⚠️ Đường dẫn hợp lệ nhưng có lỗi kết nối: {path} - {e}")
        
        # Nếu không tìm thấy database ở bất kỳ đường dẫn nào
        if self.conn is None:
            print("❌ Không tìm thấy database ở các đường dẫn thông thường")
            # Cho phép người dùng chỉ định đường dẫn
            custom_path = input("Vui lòng nhập đường dẫn đến file database: ")
            if os.path.exists(custom_path):
                try:
                    self.conn = sqlite3.connect(custom_path)
                    self.cursor = self.conn.cursor()
                    print(f"✅ Kết nối database thành công: {custom_path}")
                except sqlite3.Error as e:
                    print(f"❌ Lỗi kết nối database: {e}")
            else:
                print(f"❌ Không tìm thấy file database tại: {custom_path}")

    def close(self):
        if self.conn:
            self.conn.close()