import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print(f"Tables found: {tables}\n")

for table in tables:
    print(f"Table: {table}")
    try:
        cursor.execute(f"SELECT * FROM {table} LIMIT 5;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        if not rows:
            print("(No rows)")
    except Exception as e:
        print(f"Could not read table {table}: {e}")
    print("-" * 40)

# Print all users and their admin status
try:
    cursor.execute("SELECT username, email, is_superuser FROM auth_user;")
    users = cursor.fetchall()
    print("\nUsers in auth_user table:")
    for username, email, is_superuser in users:
        admin_status = 'Admin' if is_superuser else 'Regular User'
        print(f"Username: {username}, Email: {email}, Status: {admin_status}")
    if not users:
        print("No users found.")
except Exception as e:
    print(f"Could not read auth_user table: {e}")

conn.close()
