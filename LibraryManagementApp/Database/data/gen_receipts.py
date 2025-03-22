import sqlite3

conn = sqlite3.connect('LibraryManagementApp/Database/library.db')
c = conn.cursor()

c.execute("DELETE FROM Receipts")

receipt_list = [
    (211, 127, '9780345476517', '2025-01-18', '2025-01-22', 'Returned', '1'),
    (212, 114, '9780441788385', '2025-02-02', '2025-02-05', 'Returned', '1'),
    (213, 136, '9780671867423', '2025-01-02', '', 'Borrowed', '2'),
    (214, 164, '9780321430847', '2025-02-20', '', 'Borrowed', '1'),
    (215, 111, '9780767926034', '2025-02-25', '', 'Borrowed', '3')
]
c.executemany("insert into Receipts values(?, ?, ?, ?, ?, ?, ?)", receipt_list)
conn.commit()