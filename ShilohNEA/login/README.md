# Shiloh NEA Login System

This is a simple client-server login system using Python sockets and SQLite database.

## Project Structure

- `client/`: Contains the client application
- `server/`: Contains the server application
- `database/`: Contains database setup and data

## Setup

1. Run the database setup:
   ```
   python login/database/setup_db.py
   ```

2. Start the server:
   ```
   python login/server/server.py
   ```

3. In another terminal, run the client:
   ```
   python login/client/client.py
   ```

The client will ask for a username and password. Use the information in the database e.g  username is mike123, the password is mikepassword. ez ez ez ez ez ez ez ez ez