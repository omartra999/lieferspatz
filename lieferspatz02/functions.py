import sqlite3

##change these to own directory##
connection = r"D:\\Study\\Sems 5\\Flask\\Lieferspatz.db"
default_logo_path =r"D:\\Study\\Sems 5\\Flask\\static\\images\\r_logo.jpg"

class f:
    connection = r"D:\\Study\\Sems 5\\Flask\\Lieferspatz.db"

    def get_information(id,user_type): #get all information from database using id and user type
        conn = sqlite3.connect(connection)
        cursor = conn.cursor()
        query =  "SELECT * FROM " + user_type + " WHERE id = ?" 
        information = cursor.execute(query, (id,)).fetchone()
        return information
    def dlt_delivered(id, user_type):
        try:
            conn = sqlite3.connect(connection)
            cursor = conn.cursor()

            if user_type == 'customer':
                query = "DELETE FROM Orders WHERE customer_id = ? AND STATUS ='delivering'"
            elif user_type == 'restaurant':
                query = "DELETE FROM Orders WHERE restaurant_id = ? AND STATUS ='delivering'"
            else:
                flash('History cleared unsuccessfully', 'failed')
                return False
            print(id,query)
            cursor.execute(query, (id,))
            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False

        finally:
            if conn:
                conn.close()
