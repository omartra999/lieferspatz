import sqlite3

class registrationManager:
    def __init__(self, connection):
        self.connection = sqlite3.connect(connection)
    def userNameExists(self, username):
        with self.connection:
            query = "SELECT COUNT(*) FROM customer WHERE username = ?"
            result = self.connection.cursor().execute(query, (username,)).fetchone()[0]
            return result > 0
    
    def register(self, firstname, lastname, email, username, password,passwordConfirm, street, houseNr, plz):
            query = "INSERT INTO customer(firstname, lastname, email, username, password, street, houseNr, plz) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            parameters = (firstname, lastname, email, username, password, street, houseNr, plz)
            if self.userNameExists(username):
                return False, "username already exists"
            
            elif password != passwordConfirm:
              return False, "passwords do not match" 
            else:
                with self.connection:  
                    self.connection.cursor().execute(query, parameters)
                    return True, "user added"
