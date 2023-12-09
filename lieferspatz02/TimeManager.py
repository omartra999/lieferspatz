import sqlite3

import time
class timeManager:
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
        self.cursor = self.connection.cursor()

    def add_openning_times(self, restaurant_id, days, opens, closes):
        formatted_open_times = [time.strftime("%H:%M") for time in opens]
        formatted_close_times = [time.strftime("%H:%M") for time in closes]
        query = "INSERT INTO openning_times(restaurant_id, day, open, close) VALUES (?,?,?,?)"
        data = [(restaurant_id, day, open_time, close_time) for day, open_time, close_time in zip(days, formatted_open_times, formatted_close_times)]
        
        with self.connection:
            self.cursor.executemany(query, data)
            self.connection.commit()
            return True
            
    def get_openning_times(self, restaurant_id):
        query = "SELECT * FROM openning_times WHERE restaurant_id = ?"
        with self.connection:
            self.cursor.execute(query, (restaurant_id))
            openning_times = self.cursor.fetchall()
            return openning_times

