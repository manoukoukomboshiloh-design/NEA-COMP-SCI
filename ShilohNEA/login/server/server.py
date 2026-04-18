import sqlite3
import hashlib
import os
import socket
import threading

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'user_data.db'))


def ensure_user_table():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            '''
        )
        con.commit()


def handle_connection(client_socket):
    try:
        ensure_user_table()

        client_socket.send("Choose action: 1 for login, 2 for sign up, 3 to exit: ".encode())
        action = client_socket.recv(1024).decode().strip().lower()

        if action in {"3", "exit", "quit"}:
            client_socket.send("Goodbye!".encode())
            return

        client_socket.send("Username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        client_socket.send("Password: ".encode())
        password = client_socket.recv(1024).decode().strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()

            if action in {"2", "signup", "sign up", "register"}:
                try:
                    cur.execute(
                        "INSERT INTO userdata (username, password) VALUES (?, ?)",
                        (username, hashed_password),
                    )
                    conn.commit()
                    client_socket.send(f"Signup successful!|{cur.lastrowid}|{username}".encode())
                except sqlite3.IntegrityError:
                    client_socket.send("Signup failed! Username already exists.".encode())
                return

            cur.execute(
                "SELECT id, username FROM userdata WHERE username = ? AND password = ?",
                (username, hashed_password),
            )
            user_row = cur.fetchone()

        if user_row:
            client_socket.send(f"Login successful!|{user_row[0]}|{user_row[1]}".encode())
        else:
            client_socket.send("Login failed!".encode())
    finally:
        client_socket.close()



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 9999))
    server.listen()
    print("Server listening on localhost:9999")

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client,), daemon=True).start()


if __name__ == "__main__":
    main()