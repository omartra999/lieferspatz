import sqlite3
import json

class plzManager:
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def submit_plz_list(self, restaurant_id, plz_list):
        try:
            # Add the PLZ values from the list to the database
                with self.connection:
                    insert_query = "INSERT INTO restaurant_plz(restaurant_id, plz) VALUES (?, ?)"
                    self.cursor.execute(insert_query, (restaurant_id, plz_list,))
                self.connection.commit()
                return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_plz_list(self, restaurant_id):
        query = "SELECT plz FROM restaurant_plz WHERE restaurant_id = ?"
        with self.connection:
            self.cursor.execute(query, (restaurant_id,))
            plz_list = [plz[0] for plz in self.cursor.fetchall()]
            return plz_list
        

