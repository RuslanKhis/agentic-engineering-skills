import sqlite3

def get_profile(db, trusted_user_id):
    with sqlite3.connect(db) as connection:
        return connection.execute("SELECT language FROM profiles WHERE user_id = ?", (trusted_user_id,)).fetchone()
