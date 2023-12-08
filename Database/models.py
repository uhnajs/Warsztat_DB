from clcrypto import hash_password, check_password
import datetime

class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self.hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = "INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id"
            values = (self.username, self._hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
        else:
            sql = "UPDATE users SET username = %s, hashed_password = %s WHERE id = %s"
            values = (self.username, self._hashed_password, self._id)
            cursor.execute(sql, values)

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username = %s;"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            user_id, username, hashed_password = data
            user = User(username, password=hashed_password)
            user._id = user_id
            return user
        return None

    @staticmethod
    def load_user_by_id(cursor, user_id, hashed_pass=None):
        sql = "SELECT id, username, hashed_password FROM users WHERE id = %s"
        cursor.execute(sql, (user_id,))
        data = cursor.fetchone()
        if data:
            user_id, username, hashed_password = data
            user = User(username, password=hashed_pass)
            user._id = user_id
            return user
        return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM users"
        cursor.execute(sql)
        data_fetched = cursor.fetchall()
        users = []
        for user_data in data_fetched:
            user_id, username, hashed_password = user_data
            user =  User(username, password=hashed_password)
            user._id = user_id
            users.append(user)
        return users

    def delete(self, cursor):
        if self._id != -1:
            sql = "DELETE FROM users WHERE id = %s"
            cursor.exetue(sql, (self._id,))
            self._id = -1

    def verify_password(self, password):
        return check_password(password, self._hashed_password)



class Messages:
    def __init__(self, from_id, to_id, text, creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date if creation_date else datetime.datetime.now()

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """
            INSERT INTO messages (from_id, to_id, text, creation_date)
            VALUES (%s, %s, %s, %s) RETURNING id
            """
            values = (self.from_id, self.to_id, self.text, self.creation_date)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """
            UPDATE messages
            SET from_id = %s, to_id = %s, text = %s, creation_date = %s
            WHERE id = %s
            """
            values = (self.from_id, self.to_id, self.text, self.creation_date, self._id)
            cursor.execute(sql, values)
            return True
    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
        cursor.execute(sql)
        messages_data = cursor.fetchall()
        messages = []
        for message_data in messages_data:
            message_id, from_id, to_id, text, creation_date = message_data
            message = Messages(from_id, to_id, text, creation_date)  # Zmiana tutaj
            message._id = message_id
            messages.append(message)
        return messages