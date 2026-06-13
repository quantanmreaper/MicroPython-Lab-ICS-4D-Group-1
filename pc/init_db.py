#ICS GROUP 4D GROUP 1 EMBEDDED SYSTEMS AND IOT
import sqlite3

DB_FILE = "readings.db"


def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS readings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity    REAL,
            timestamp   TEXT
        )
        """
    )

    conn.commit()
    conn.close()
    print("OK: database '{}' is ready with table 'readings'.".format(DB_FILE))


if __name__ == "__main__":
    create_database()
