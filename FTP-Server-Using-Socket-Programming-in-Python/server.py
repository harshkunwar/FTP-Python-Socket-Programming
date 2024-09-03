import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4469
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"  # Path where files are saved on the server

# Automatically create the 'server_data' folder if it doesn't exist
if not os.path.exists(SERVER_DATA_PATH):
    os.makedirs(SERVER_DATA_PATH)

user_credentials = {
    "alice": "password123",
    "bob": "securepass",
    "charlie": "letmein",
    "dave": "secretword",
    "eve": "123456",
    "frank": "qwerty",
    "grace": "ilovepython",
    "harry": "mypassword",
    "irene": "p@ssw0rd",
    "jason": "pythonrocks"
}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    d = "OK@Welcome to the File Server Login Page."
    conn.send(d.encode(FORMAT))

    dta = conn.recv(SIZE).decode(FORMAT)
    dta = dta.split("@")
    cd = dta[0]

    # User authentication
    if cd in user_credentials:
        if dta[1] == user_credentials.get(cd):
            send_daa = "OK@Authenticated"
        else:
            send_daa = "False"
    else:
        send_daa = "False"
    conn.send(send_daa.encode(FORMAT))
    
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))
    
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        # List files in server_data directory
        if cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        # Upload a file to server_data directory
        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)
            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))

        # Delete a file from server_data directory
        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]
            if len(files) == 0:
                send_data += "The Server is empty"
            else:
                if filename in files:
                    os.remove(f"{SERVER_DATA_PATH}/{filename}")
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."
            conn.send(send_data.encode(FORMAT))

        # Help command listing available commands
        elif cmd == "HELP":
            data = "OK@"
            data += "LIST: List all the files from the server.\n"
            data += "UPLOAD <filename> <text>: Upload a file to the server.\n"
            data += "DELETE <filename>: Delete a file from the server.\n"
            data += "LOGOUT: Disconnect from the server.\n"
            data += "HELP: List all the commands."
            conn.send(data.encode(FORMAT))

        # Client logout
        elif cmd == "LOGOUT":
            break

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
