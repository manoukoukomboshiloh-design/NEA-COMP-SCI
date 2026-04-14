import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()


def get_user(username):
    con = sqlite3.connect("../database/userdata.db")
    cur  = con.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
    result = cur.fetchone()
    con.close()
    return result



def handle_connection(client_socket):
    client_socket.send("Username: ".encode())
    username = client_socket.recv(1024).decode().strip()
    client_socket.send("Password: ".encode())
    password = client_socket.recv(1024).decode().strip()
    password = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect("../database/userdata.db")
    cur = conn.cursor() 
    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

    if cur.fetchall():
        client_socket.send("Login successful!".encode())    
        # Display user dashboard with progress bars and stats
    else:
        client_socket.send("Login failed!".encode())

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()