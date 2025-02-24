import sqlite3
import random
import faker
import unidecode

connect = sqlite3.connect('C:/Users/Admin/Documents/1. HỌC TẬP/5. KỸ THUẬT LẬP TRÌNH/3. FINAL PROJECT/database.db')
cursor = connect.cursor()

fake = faker.Faker("vi_VN")

ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Đặng", "Bùi", "Đỗ", "Hồ"]
ten_dem = ["Văn", "Hữu", "Quang", "Minh", "Ngọc", "Thị", "Bích", "Xuân", "Thanh", "Trọng"]
ten = ["Nam", "Hải", "Dương", "Linh", "Trang", "Hùng", "Tùng", "Anh", "Thảo", "Lan"]

usernames = set()
emails = set()

def email(name, user_id):
    ten_parts = name.split()
    short_name = "".join([unidecode.unidecode(word[0]).lower() for word in ten_parts[:-1]])
    last_name = unidecode.unidecode(ten_parts[-1]).lower()
    user = last_name.lower() + short_name.lower() + user_id
    email = f"{last_name.lower()}{short_name.lower()}{user_id}@user.libma"
    if email not in emails:
        emails.add(email)
    return user, email

users_data = []
start_id = 117
for i in range(51):
    user_id = f"0{start_id + i}"
    name = random.choice(ho) + " " + random.choice(ten_dem) + " " + random.choice(ten)
    user, mail = email(name, user_id)
    password = '123456789'
    date_of_birth = fake.date_of_birth(minimum_age=10, maximum_age=70).strftime("%Y-%m-%d")
    role = "User"
    users_data.append((user_id, name, user, mail, password, date_of_birth, role))

cursor.executemany("INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?, ?, ?, ?)", users_data)
connect.commit()