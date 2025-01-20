import sqlite3

try:
    conn = sqlite3.connect(
        'db.sqlite3'
    )
except sqlite3.Error as e:
    print(e)

cursor = conn.cursor()

#History of cart/trolley/checkout
res = cursor.execute("SELECT id, ordered, quantity, item_id, user_id FROM catalog_orderitem")

for row in res:
    line = res.fetchone()
    print(line)

conn.close()
