import argparse
from psycopg2 import connect, OperationalError, errors
from models import User
from clcrypto import check_password, hash_password

db_parameters = {
    'dbname': 'exercise_db',
    'user': 'postgres',
    'password': 'coderslab',
    'host': 'localhost',
    'port': '5433'
}

def create_user(username, password):
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return
    try:
        with connect(**db_parameters) as conn:
            with conn.cursor() as cursor:
                new_user = User(username, password)
                new_user.save_to_db(cursor)
                conn.commit()
                print(f"User {username} created successfully.")
    except errors.UniqueViolation:
        print(f"User {username} already exists.")

def change_password(username, old_password, new_password):
    if len(new_password) < 8:
        print("New password must be at least 8 characters long.")
        return
    try:
        with connect(**db_parametrs) as conn:
            with conn.cursor() as cursor:
                user = User.load_user_by_username(cursor, username)
                if user and check_password(old_password, user.hashed_password):
                    user.set_password(new_password)
                    user.save_to_db(cursor)
                    conn.commit()
                    print("Password updated successfully.")
                else:
                    print("Invalid username or password.")
    except OperationalError as err:
        print(f"Database error:{err}")

def delete_user(username, password):
    try:
        with connect(**db_parametrs) as conn:
            with conn.cursor() as cursor:
                user = User.load_user_by_username(cursor, username)
                if user and check_password(password, user.hashed_password):
                    user.delete(cursor)
                    conn.commit()
                    print(f"User {username} deleted sucessfully.")
                else:
                    print("Invalid username or password.")
    except OperationalError as err:
        print(f"Database error: {err}")

def list_users():
    try:
        with connect(**db_parametrs) as conn:
            with conn.cursor() as cursor:
                users = User.load_all_users(cursor)
                for user in users:
                    print(f"ID: {user.id}, Username: {user.username}")
    except OperationalError as err:
        print(f"Database error: {err}")

parser = argparse.ArgumentParser(description="User management application")
parser.add_argument("-u", "--username", help="Username")
parser.add_argument("-p", "--password", help="User password")
parser.add_argument("-n", "--new_pass", help="New password for user")
parser.add_argument("-l", "--list", action="store_true", help="List users")
parser.add_argument("-d", "--delete", action="store_true", help="Delete user")
parser.add_argument("-e", "--edit", action="store_true", help="Edit user")

args = parser.parse_args()

if args.list:
    list_users()
elif args.delete and args.username and args.password:
    delete_user(args.username, args.password)
elif args.edit and args.username and args.password:
    change_password(args.username, args.password, args.new_pass)
elif args.username and args.password:
    if not args.edit and not args.delete:
        create_user(args.username, args.password)
else:
    parser.print_help()