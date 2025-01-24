import sqlite3


async def add_autoreply(user_id) -> None:
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        query = "INSERT INTO Profi (id, mod) VALUES (?, ?);"
        cursor.execute(query, (user_id, "True"))
        db.commit()



async def del_autoreply(user_id: int) -> None:
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        query = "DELETE FROM Profi WHERE id = ?;"
        cursor.execute(query, (user_id, ))
        db.commit()


async def select_all_autoreply():
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        query = "SELECT * FROM Profi"
        cursor.execute(query)
        data = cursor.fetchall()
        db.commit()
        return data







