import sqlite3

conn = sqlite3.connect('LibraryManagementApp/Database/library.db')
c = conn.cursor()

receipt_list = [
    (211, 127, '0345417623', '2025-01-18', '2025-01-22', 'Returned', '1'),
    (212, 114, '0060168013', '2025-02-02', '2025-02-05', 'Returned', '1'),
    (213, 136, '0345465083', '2025-02-02', '', 'Overdue', '1'),
    (214, 164, '0743403843', '2025-02-20', '', 'Borrowed', '1'),
    (215, 111, '0553584383', '2025-02-25', '', 'Borrowed', '1')
]
c.executemany("insert into Receipts values(?, ?, ?, ?, ?, ?, ?)", receipt_list)
conn.commit()