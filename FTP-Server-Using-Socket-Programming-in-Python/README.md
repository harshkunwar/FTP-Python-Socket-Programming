# FTP Server Using Socket Programming in Python

This project provides a basic FTP server implemented with socket programming in Python. The client connects to the server, authenticates with a username and password, and can perform essential file operations such as listing, uploading, and deleting files.

## Features

- **Authentication**: Clients need to log in with a username and password before accessing other functionalities.
- **File Operations**:
  - **LIST**: Retrieve a list of all files available on the server.
  - **UPLOAD**: Upload a file to the server.
  - **DELETE**: Remove a file from the server.
  - **LOGOUT**: Disconnect from the server.
  - **HELP**: Show a list of commands that can be used.

## Prerequisites

- Python 3.x
- Tkinter library (for client-side GUI).
- Both client and server must be on the same network.

## Getting Started

### Setting Up the Server

1. Clone the repository to your server machine.
2. Ensure a `server_data` directory exists in the same location as `server.py`. If needed, update the `SERVER_DATA_PATH` variable in `server.py` to reflect the directory where files should be stored.
3. Execute `server.py` to launch the server.

### Setting Up the Client

1. Clone the repository to your client machine.
2. Modify the `client.py` file to set the `IP` variable to the server's IP address.
3. Confirm that the `client_data` directory is in the same directory as `client.py`, or adjust the path to the directory from which you wish to upload files.
4. Run `client.py` to connect to the server.

## Usage

1. **Authentication:**

   - Upon running the client, a login window will prompt you for your username and password.

2. **Credentials:**

   - The following default usernames and passwords are used:
     - `alice: password123`
     - `bob: securepass`
     - `charlie: letmein`
     - `dave: secretword`
     - `eve: 123456`
     - `frank: qwerty`
     - `grace: ilovepython`
     - `harry: mypassword`
     - `irene: p@ssw0rd`
     - `jason: pythonrocks`
   - Modify or add credentials in `server.py` as needed.

3. **Commands:**

   - After logging in, you can use these commands:
     - **LIST**: Display all files stored on the server.
     - **UPLOAD `<path>`**: Upload a file from the specified path to the server.
     - **DELETE `<filename>`**: Remove a file from the server by its filename.
     - **LOGOUT**: End the connection to the server.
     - **HELP**: List all available commands.

## Example

### Server Output

