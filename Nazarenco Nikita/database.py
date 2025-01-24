import sqlite3


def add_autoreply(user_id) -> None:
    with sqlite3.connect("../database.db") as db:
        cursor = db.cursor()
        query = "INSERT INTO Profi (id, mod) VALUES (?, ?);"
        cursor.execute(query, (user_id, "True"))
        db.commit()



def del_autoreply(user_id: int) -> None:
    with sqlite3.connect("../database.db") as db:
        cursor = db.cursor()
        query = "DELETE FROM Profi WHERE id = ?;"
        cursor.execute(query, (user_id, ))
        db.commit()


def check_autoreply(user_id: int):
    with sqlite3.connect("../database.db") as db:
        cursor = db.cursor()
        query = "SELECT mod FROM Profi WHERE id = ?;"
        cursor.execute(query, (user_id, ))
        data = cursor.fetchone()
        db.commit()
        return data


def check_is_first(user_id, id_profi):
    with sqlite3.connect("../database.db") as db:
        cursor = db.cursor()
        query = "SELECT is_first FROM Users WHERE id = ? AND id_profi = ?;"
        cursor.execute(query, (user_id, id_profi))
        data = cursor.fetchone()
        db.commit()
        return data

def add_users(user_id, id_profi) -> None:
    with sqlite3.connect("../database.db") as db:
        cursor = db.cursor()
        query = "INSERT INTO Users (id, is_first, id_profi) VALUES (?, ?, ?);"
        cursor.execute(query, (user_id, "True", id_profi))
        db.commit()


def zeroing_users(id_profi):
    with sqlite3.connect("../database.db") as db:
        cursor = db.cursor()
        query = "UPDATE Users SET is_first = ? WHERE id_profi = ?;"
        cursor.execute(query, ("FALSE", id_profi))
        db.commit()






