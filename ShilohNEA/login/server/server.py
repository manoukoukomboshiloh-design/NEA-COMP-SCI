import sqlite3
import hashlib
import os
import socket
import threading

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'userdata.db'))


def get_user(username):
    con = sqlite3.connect(DB_PATH)
    cur  = con.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
    result = cur.fetchone()
    con.close()
    return result



def handle_connection(client_socket):
    try:
        client_socket.send("Username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        client_socket.send("Password: ".encode())
        password = client_socket.recv(1024).decode().strip()
        password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM userdata WHERE username = ? AND password = ?", (username, password))
        user_row = cur.fetchone()
        conn.close()

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