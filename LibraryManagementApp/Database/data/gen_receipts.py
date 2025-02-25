import sqlite3

conn = sqlite3.connect('LibraryManagementApp/Database/library.db')
c = conn.cursor()

receipt_list = [
    (211, 127, 1900850303, '2025-01-18', '2025-01-22', 'Returned'),
    (212, 114, 156047624, '2025-02-02', '2025-02-05', 'Returned'),
    (213, 136, 966986105, '2025-02-02', '', 'Overdue'),
    (214, 164, 312953453, '2025-02-20', '', 'Borrowed'),
    (215, 111, 316973742, '2025-02-25', '', 'Borrowed')
]
c.executemany("insert into Receipts values(?, ?, ?, ?, ?, ?)", receipt_list)
conn.commit()