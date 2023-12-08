from psycopg2 import connect
from models import User, Messages  # Upewnij się, że importujesz Messages z odpowiedniego miejsca

# Nawiąż połączenie z bazą danych
db_params = {
    'dbname': 'exercise_db',
    'user': 'postgres',
    'password': 'coderslab',
    'host': 'localhost',
    'port': '5433'
}

connection = connect(**db_params)

# Utwórz kursor
cursor = connection.cursor()

# Dodaj użytkowników do bazy danych
user1 = User(username='user1', password='password1')
user1.save_to_db(cursor)
user2 = User(username='user2', password='password2')
user2.save_to_db(cursor)


# Zakładamy, że użytkownicy o id 1 i 2 już istnieją w bazie danych
from_id = 1
to_id = 2
text = "Hello, this is a test message."

# Utwórz nowy obiekt Messages i zapisz go w bazie danych
new_message = Messages(from_id, to_id, text)
new_message.save_to_db(cursor)
print(f"New message ID: {new_message.id}")

# Załaduj wszystkie wiadomości z bazy danych
loaded_messages = Messages.load_all_messages(cursor)
for message in loaded_messages:
    print(f"Message ID: {message.id}, From: {message.from_id}, To: {message.to_id}, Text: '{message.text}'")

# Zatwierdź zmiany w bazie danych
connection.commit()

# Zamknij kursor i połączenie
cursor.close()
connection.close()
