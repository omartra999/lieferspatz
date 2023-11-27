import sqlite3

class loginManager:
    def __init__(self,connection):
        self.connection =sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def login(self, username, password):
        query = "SELECT COUNT(*) FROM customer WHERE username = ? AND password = ?"
        with self.connection:
            result = self.cursor.execute(query,(username, password,)).fetchone()[0]
            if result > 0:
                return True
    ##add a restaurant log in function to also return boolean
