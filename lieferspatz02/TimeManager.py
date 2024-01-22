import sqlite3
class timeManager:
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def dayExists(self, restaurant_id, day):
        try:
            with self.connection:
                query = "SELECT COUNT (*) FROM openning_times WHERE restaurant_id = ? AND day = ?"
                self.cursor.execute(query, restaurant_id, day,)
                count = self.cursor.fetchone()[0]
                return count > 0
        except Exception as e:
            print(f"an error accured: {e}")
            return False

    def add_openning_times(self, restaurant_id, days, opens, closes):
        print(f"extracted restaurant id form session : {restaurant_id}")
        try:
            with self.connection:
                insertQuery = "INSERT INTO openning_times(restaurant_id, day, open, close) VALUES (?,?,?,?)"
                for day, open, close in zip(days, opens, closes):
                    if self.dayExists(restaurant_id, day) == False:
                        exec = (restaurant_id, day, open, close,)
                        self.cursor.execute(insertQuery, (exec))
                    self.connection.commit()
                return True
        except Exception as e:
            print(f"An error accured: {e}")
            return False
                    
                    
    def get_openning_times(self, restaurant_id):
        query = "SELECT * FROM openning_times WHERE restaurant_id = ?"
        with self.connection:
            self.cursor.execute(query, (restaurant_id,))
            openning_times = self.cursor.fetchall()
            return openning_times

    def set_openning_times(self, restaurant_id, days, opens, closes):
        print(f"extracted restaurant id form session : {restaurant_id}")
        try:
            #delete existing times
            with self.connection:
                deleteQuery = "DELETE FROM openning_times WHERE restaurant_id = ?"
                self.cursor.execute(deleteQuery, (restaurant_id,))
            
            #add the new times
            with self.connection:
                insertQuery = "INSERT INTO openning_times(restaurant_id, day, open, close) VALUES (?,?,?,?)"
                for day, open, close in zip(days, opens, closes):
                    if self.dayExists(restaurant_id, day) == False:
                        self.cursor.execute(insertQuery, (restaurant_id, day, open, close,))
                    self.connection.commit()

            return True
        except Exception as e :
            print(f"an error accured: {e}")
            return False
