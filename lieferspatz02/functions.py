import sqlite3

connection = r"D:\\Study\\Sems 5\\Flask\\Lieferspatz.db"


class f:
    connection = r"D:\\Study\\Sems 5\\Flask\\Lieferspatz.db"

    def get_information(id,user_type): #get all information from database using id and user type
        conn = sqlite3.connect(connection)
        cursor = conn.cursor()
        query =  "SELECT * FROM " + user_type + " WHERE id = ?" 
        information = cursor.execute(query, (id,)).fetchone()
        return information