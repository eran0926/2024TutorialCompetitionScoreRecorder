import mariadb
import sys

match_level_table = ["Practice", "Qualification", "Playoff"]
level_to_num = {"Practice": 0, "Qualification": 1, "Playoff": 2}

match_state_table = ["Not Started", "Preparing",
                     "Running", "Ended", "All Commited", "Saved", "Interrupted"]
state_to_num = {
    "Not Started": 0,
    "Preparing": 1,
    "Running": 2,
    "Ended": 3,
    "All Commited": 4,
    "Saved": 5,
    "Interrupted": 6
}


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
    return conn


class DBOperator:
    def __init__(self):
        pass
        # self.cur = connect()

    def login_query(self, username, password):
        """Retrieves the user data from the database"""
        with connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

            return cur.fetchall()

    def get_all_users(self):
        """Retrieves all users from the database"""
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")

            return cur.fetchall()

    def get_all_username(self):
        """Retrieves all username from the database"""
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT username FROM users")

            return [i[0] for i in cur.fetchall()]

    def get_user(self, username):
        """Retrieves a user from the database"""
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))

            return cur.fetchone()

    def get_matches_info(self):
        """Retrieves all matches from the database"""
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM match_info")

            matches_info = list(cur.fetchall())
            for index, match_info in enumerate(matches_info):
                matches_info[index] = list(match_info)
                matches_info[index][0] = match_level_table[match_info[0]]
                matches_info[index][6] = match_state_table[match_info[6]]

            return matches_info

    def load_match_data(self, match_level, match_id):
        """Retrieves a match from the database"""
        with connect() as conn:
            cur = conn.cursor()

            match_level = level_to_num[match_level]

            cur.execute(
                "SELECT * FROM match_info WHERE level = ? AND id = ?", (match_level, match_id))

            match_info = cur.fetchone()
            match_info = list(match_info)
            match_info[0] = match_level_table[match_info[0]]
            match_info[6] = match_state_table[match_info[6]]

            return match_info

    def change_match_state(self, match_level, match_id, state):
        """Change match state in the database"""
        with connect() as conn:
            cur = conn.cursor()
            if type(state) == str and state in state_to_num.keys():
                state = state_to_num[state]

            match_level = level_to_num[match_level]

            cur.execute(
                "UPDATE match_info SET state = ? WHERE level = ? AND id = ?", (state, match_level, match_id))

    def reset_other_loaded_match_state(self, match_level, match_id):
        """Reset other loaded match state in the database"""
        with connect() as conn:
            cur = conn.cursor()

            match_level = level_to_num[match_level]

            cur.execute(
                "UPDATE match_info SET state = ? WHERE level != ? OR id != ? AND state = ?", (0, match_level, match_id, 1))

    def save_match_data(self, match_data):
        """Save match data to the database"""
        sql_query_head = "INSERT INTO match_result ("
        sql_value_tuple = []
        for i in match_data:
            if i["id"] == "match-level":
                i["value"] = level_to_num[i["value"]]
            sql_query_head += "`" + i["id"] + "`,"
            sql_value_tuple.append(i["value"])
        sql_query = sql_query_head[:-1] + \
            ") VALUES (" + "?,"*(len(match_data)-1) + "?)"
        print(sql_query)
        print(sql_value_tuple)
        with connect() as conn:
            cur = conn.cursor()

            cur.execute(sql_query, tuple(sql_value_tuple))


if __name__ == "__main__":
    db = DBOperator()
    print(db.get_all_users())
    print(db.get_all_username())
    print(db.get_user("'"))
