import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash



BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "users.db"
)



def create_database():

    os.makedirs(
        os.path.dirname(DATABASE_PATH),
        exist_ok=True
    )


    with sqlite3.connect(DATABASE_PATH) as connection:


        cursor = connection.cursor()



        cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT NOT NULL,

            role TEXT NOT NULL

        )
        """
        )



        users = [

            (
                "admin",
                "admin123",
                "admin"
            ),

            (
                "teacher",
                "teacher123",
                "teacher"
            ),

            (
                "student",
                "student123",
                "student"
            )

        ]



        for user in users:

            try:

                cursor.execute(

                """
                INSERT INTO users
                (username,password,role)

                VALUES(?,?,?)

                """,

                (
                    user[0],
                    generate_password_hash(user[1]),
                    user[2]
                )

                )


            except sqlite3.IntegrityError:

                pass



        connection.commit()




def verify_user(username, password):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, password, role
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    if user:
        if check_password_hash(
            user[2],
            password
        ):
            return {
                "id": user[0],
                "username": user[1],
                "role": user[3]
            }

    return None

def add_user(username, password, role):
    """
    Add a new user to the database.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
            """,
            (
                username,
                generate_password_hash(password),
                role
            )
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()






def get_all_users():
    """
    Return all users.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, username, role FROM users"
    )

    users = cursor.fetchall()

    connection.close()

    return users


def update_password(username, new_password):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            return False

        cursor.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (
                generate_password_hash(new_password),
                username
            )
        )
        connection.commit()
        return True
    finally:
        connection.close()