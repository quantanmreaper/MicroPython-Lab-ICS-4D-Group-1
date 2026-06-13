#ICS GROUP 4D GROUP 1 EMBEDDED SYSTEMS AND IOT

"""
view_data.py  -- This is our  quick way to see what is stored in the database.
"""

import sqlite3

DB_FILE = "readings.db"


def show_recent(limit=20):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
    print("Total readings stored:", total)
    print("-" * 55)
    print("{:>4}  {:>8}  {:>8}  {:<19}".format("id", "temp", "hum", "timestamp"))
    print("-" * 55)

    rows = cursor.execute(
        "SELECT id, temperature, humidity, timestamp "
        "FROM readings ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()

    for row in rows:
        row_id, temp, hum, ts = row
        print("{:>4}  {:>8}  {:>8}  {:<19}".format(row_id, temp, hum, ts))

    conn.close()


if __name__ == "__main__":
    show_recent()
