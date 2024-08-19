import mariadb
import sys
import os

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

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_USER = os.getenv("DB_USER", "counter")
DB_PASSWORD = os.getenv("DB_PASSWORD", "counter")
DB_DATABASE = os.getenv("DB_DATABASE", "counter_db")


def connect(**kwargs):
    try:
        conn = mariadb.connect(
            user=kwargs.get("user", DB_USER),
            password=kwargs.get("password", DB_PASSWORD),
            host=kwargs.get("host", DB_HOST),
            port=kwargs.get("port", DB_PORT),
            database=kwargs.get("database", DB_DATABASE)
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    conn.autocommit = kwargs.get("autocommit", True)
    return conn


class DBOperator:
    def __init__(self):
        pass
        # self.cur = connect()

    def check_tables(self):
        with connect(autocommit=False) as conn:
            cur = conn.cursor()
            cur.execute("SHOW TABLES")
            tables = cur.fetchall()
            print(tables)
            if ('users',) not in tables:
                cur.execute(
                    "CREATE TABLE `users` (  `id` int(11) NOT NULL,  `username` char(20) NOT NULL,  `password` char(20) NOT NULL,  `role` int(11) NOT NULL,  `alliance` char(5) NOT NULL);")
                cur.execute("INSERT INTO `users` (`id`, `username`, `password`, `role`, `alliance`) VALUES(1, 'r1', '1', 1, 'red'),(2, 'r2', '1', 1, 'red'),(3, 'b1', '1', 1, 'blue'),(4, 'b2', '1', 1, 'blue'),(5, 'admin', 'admin', 0, '');")
                cur.execute(
                    "ALTER TABLE `users`  ADD PRIMARY KEY (`id`) USING BTREE;")
                cur.execute(
                    "ALTER TABLE `users`  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;")
            if ('match_info',) not in tables:
                cur.execute("CREATE TABLE `match_info` (  `level` int(11) NOT NULL DEFAULT 2,  `id` int(11) NOT NULL,  `red1` char(8) NOT NULL,  `red2` char(8) NOT NULL,  `blue1` char(8) NOT NULL,  `blue2` char(8) NOT NULL,  `state` int(11) NOT NULL DEFAULT 0);")
                cur.execute(
                    "ALTER TABLE `match_info` ADD PRIMARY KEY (`level`,`id`);")
            if ('match_result',) not in tables:
                cur.execute("CREATE TABLE `match_result` (  `match-level` int(11) NOT NULL,  `match-id` int(11) NOT NULL,  `red-team1` char(8) NOT NULL,  `blue-team1` char(8) NOT NULL,  `red-team2` char(8) NOT NULL,  `blue-team2` char(8) NOT NULL,  `red-total-score-with-penalty` int(11) NOT NULL,  `blue-total-score-with-penalty` int(11) NOT NULL,  `red-melody` tinyint(1) NOT NULL,  `blue-melody` tinyint(1) NOT NULL,  `red-melody-demand` int(11) NOT NULL,  `blue-melody-demand` int(11) NOT NULL,  `red-ensemble` tinyint(1) NOT NULL,  `blue-ensemble` tinyint(1) NOT NULL,  `red-ensemble-demand` int(11) NOT NULL,  `blue-ensemble-demand` int(11) NOT NULL,  `winner` char(4) NOT NULL,  `red-auto-leave1` int(11) NOT NULL,  `blue-auto-leave1` int(11) NOT NULL,  `red-auto-leave2` int(11) NOT NULL,  `blue-auto-leave2` int(11) NOT NULL,  `red-auto-leavePoints` int(11) NOT NULL,  `blue-auto-leavePoints` int(11) NOT NULL,  `red-auto-speaker` int(11) NOT NULL,  `blue-auto-speaker` int(11) NOT NULL,  `red-auto-echo` int(11) NOT NULL,  `blue-auto-echo` int(11) NOT NULL,  `red-auto-foul` int(11) NOT NULL,  `blue-auto-foul` int(11) NOT NULL,  `red-auto-techFoul` int(11) NOT NULL,  `blue-auto-techFoul` int(11) NOT NULL,  `red-auto-total-point` int(11) NOT NULL,  `blue-auto-total-point` int(11) NOT NULL,  `red-telop-speaker` int(11) NOT NULL,  `blue-telop-speaker` int(11) NOT NULL,  `red-telop-echo` int(11) NOT NULL,  `blue-telop-echo` int(11) NOT NULL,  `red-telop-fortissimo` int(11) NOT NULL,  `blue-telop-fortissimo` int(11) NOT NULL,  `red-telop-foul` int(11) NOT NULL,  `blue-telop-foul` int(11) NOT NULL,  `red-telop-techFoul` int(11) NOT NULL,  `blue-telop-techFoul` int(11) NOT NULL,  `red-telop-park1` int(11) NOT NULL,  `blue-telop-park1` int(11) NOT NULL,  `red-telop-park2` int(11) NOT NULL,  `blue-telop-park2` int(11) NOT NULL,  `red-telop-stagePoints` int(11) NOT NULL,  `blue-telop-stagePoints` int(11) NOT NULL,  `red-telop-total-point` int(11) NOT NULL,  `blue-telop-total-point` int(11) NOT NULL,  `red-total-score` int(11) NOT NULL,  `blue-total-score` int(11) NOT NULL,  `red-total-penalty` int(11) NOT NULL,  `blue-total-penalty` int(11) NOT NULL);")
            if ('rankings',) not in tables:
                cur.execute("CREATE TABLE `rankings` (  `team-number` char(8) NOT NULL,  `ranking-points` int(11) NOT NULL DEFAULT 0,  `average-points` double(10,0) NOT NULL DEFAULT 0,  `average-auto-points` double(10,0) NOT NULL DEFAULT 0,  `win` int(11) NOT NULL DEFAULT 0,  `lose` int(11) NOT NULL DEFAULT 0,  `tie` int(11) NOT NULL DEFAULT 0);")
                cur.execute(
                    "ALTER TABLE `rankings` ADD PRIMARY KEY (`team-number`);")
            conn.commit()

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
                "UPDATE match_info SET state = ? WHERE (level != ? OR id != ?) AND state = ?", (0, match_level, match_id, 1))

    def get_match_times(self, team_number):
        """Retrieves match times from the database"""
        with connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM match_result WHERE `match-level` = ? AND (`red-team1` = ? OR `red-team2` = ? OR `blue-team1` = ? OR `blue-team2` = ?)", (1, team_number, team_number, team_number, team_number))
            return len(cur.fetchall())

    def get_team_rank(self, team_number):
        """Retrieves team rank from the database"""
        with connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM rankings WHERE `team-number` = ?", (team_number,))
            return cur.fetchone()

    def update_team_rank(self, team_number, rank):
        """Update team rank in the database"""
        rank = tuple(rank)
        with connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO rankings (`team-number`, `ranking-points`, `average-points`, `average-auto-points`, `win`, `lose`, `tie`) VALUES (?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE `ranking-points` = ?, `average-points` = ?, `average-auto-points` = ?, `win` = ?, `lose` = ?, `tie` = ?", rank+rank[1:])
# TODO

    def get_all_team_rank(self):
        """Retrieves all team rank from the database"""
        with connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM rankings")
            return list(cur.fetchall())

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
