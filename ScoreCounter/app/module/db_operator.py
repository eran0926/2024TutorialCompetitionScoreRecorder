import mariadb
import sys

match_level = ["Practice", "Qualification", "Playoff"]
match_state = ["Not Started", "Preparing", "Running", "Ended"]


def connect():
    try:
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="counter_db"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    conn.autocommit = True
    return conn.cursor()

# Get Cursor


# def loginQuery(cur, username, password):
#     """Retrieves the user data from the database"""

#     cur.execute(
#         "SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

#     return cur


# def get_all_users(cur):
#     """Retrieves all users from the database"""

#     cur.execute("SELECT username FROM users")

#     return cur.fetchall()


def add_user(cur, username, password, role, alliance):
    """Adds a new user to the database"""

    cur.execute(
        "INSERT INTO users (username, password, role, alliance) VALUES (?, ?, ?, ?)", (username, password, role, alliance))

    return cur


class DBOperator:
    def __init__(self):
        self.cur = connect()

    def login_query(self, username, password):
        """Retrieves the user data from the database"""

        self.cur.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

        return self.cur.fetchall()

    def get_all_users(self):
        """Retrieves all users from the database"""

        self.cur.execute("SELECT * FROM users")

        return self.cur.fetchall()

    def get_all_username(self):
        """Retrieves all username from the database"""

        self.cur.execute("SELECT username FROM users")

        return [i[0] for i in self.cur.fetchall()]

    def get_user(self, username):
        """Retrieves a user from the database"""

        self.cur.execute("SELECT * FROM users WHERE username = ?", (username,))

        return self.cur.fetchone()

    def get_matches_info(self):
        """Retrieves all matches from the database"""

        self.cur.execute("SELECT * FROM match_info")

        matches_info = list(self.cur.fetchall())
        print(matches_info)
        for index, match_info in enumerate(matches_info):
            matches_info[index] = list(match_info)
            matches_info[index][0] = match_level[match_info[0]]
            matches_info[index][6] = match_state[match_info[6]]

        return matches_info

    def load_match_data(self, match_level, match_id):
        """Retrieves a match from the database"""

        self.cur.execute(
            "SELECT * FROM match_info WHERE level = ? AND id = ?", (match_level, match_id))

        match_info = self.cur.fetchone()
        match_info = list(match_info)
        match_info[0] = match_level[match_info[0]]
        match_info[6] = match_state[match_info[6]]

        return match_info

    def close(self):
        self.cur.close()


if __name__ == "__main__":
    db = DBOperator()
    print(db.get_all_users())
    print(db.get_all_username())
    print(db.get_user("'"))
