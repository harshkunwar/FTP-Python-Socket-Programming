import socket
import tkinter as tk

# Server connection details
IP="10.38.2.139"  # IP address of the server
PORT = 4469       # Port number on which the server is listening
ADDR = (IP, PORT) # Tuple containing IP and PORT to use for connection
FORMAT = "utf-8"  # Data encoding format (UTF-8)
SIZE = 1024       # Buffer size for receiving data (1024 bytes)

# Function to authenticate the client with the server
def authenticate(client, username, password):
    # Send the username and password in the format: "username@password"
    data = f"{username}@{password}"
    client.send(data.encode(FORMAT))  # Send the encoded credentials to the server
    
    # Receive and decode the server's response
    response = client.recv(SIZE).decode(FORMAT)
    
    # Check if authentication is successful
    if response == "OK@Authenticated":
        print("Authentication successful")
        return True  # Return True if authenticated
    else:
        print("Authentication failed. Please try again.")
        return False  # Return False if authentication failed

# Function to display a GUI for getting user credentials (username and password)
def get_credentials():
    def submit():
        # Get username and password entered by the user and close the window
        nonlocal username, password
        username = username_entry.get()
        password = password_entry.get()
        root.destroy()  # Close the Tkinter window
    
    # Initialize username and password as None
    username=None
    password=None

    # Create the Tkinter window for login
    root = tk.Tk()
    root.title("Login")  # Set window title
    root.geometry("250x100")  # Set window size (width x height)

    # Create and place the username label and entry field
    username_label = tk.Label(root, text="Username:")
    username_label.grid(row=0, column=0, sticky="e")  # Label position
    username_entry = tk.Entry(root, width=15)  # Username input field
    username_entry.grid(row=0, column=1)  # Field position
    username_entry.config(font=("Times New Roman", 15))  # Font configuration

    # Create and place the password label and entry field (password is hidden using 'show' parameter)
    password_label = tk.Label(root, text="Password:")
    password_label.grid(row=1, column=0, sticky="e")  # Label position
    password_entry = tk.Entry(root, show="*", width=15)  # Password input field (masked)
    password_entry.grid(row=1, column=1)  # Field position
    password_entry.config(font=("Times New Roman", 15))  # Font configuration

    # Create and place the submit button
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=2, columnspan=2, pady=20, padx=10)  # Button position and padding

    root.mainloop()  # Start the Tkinter event loop to display the window
    return username, password  # Return the entered username and password

# Main function to connect to the server and handle client operations
def main():
    # Create a new socket object for the client using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)  # Connect to the server using the specified address

    # Receive the initial message from the server
    dta = client.recv(SIZE).decode(FORMAT)  # Receive and decode the message
    cd, messag = dta.split("@")  # Split the message into command (cd) and message (messag)
    
    # Check if the server sends a disconnection message
    if cd == "DISCONNECTED":
        print(f"[SERVER]: {messag}")  # Print the disconnection message
        return  # Exit the function if disconnected
    elif cd == "OK":
        print(f"{messag}")  # Print the welcome message from the server
    
    # Get the username and password from the user using the Tkinter GUI
    username, password = get_credentials()

    # Attempt to authenticate the user with the server
    a = authenticate(client, username, password)
    if a == False:
        return  # Exit the function if authentication fails
    
    # Main loop to interact with the server after successful authentication
    while True:
        # Receive and decode the server's response
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")  # Split the response into command (cmd) and message (msg)
        
        # If the server sends a disconnection command, break the loop
        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")  # Print the disconnection message
            break  # Exit the loop
        
        # If the server sends a normal response, print the message
        elif cmd == "OK":
            print(f"{msg}")
        
        # Get the user input for the next command (e.g., LIST, UPLOAD, DELETE, LOGOUT)
        data = input("> ")
        data = data.split(" ")  # Split the input into command and arguments
        cmd = data[0]  # The first word is the command

        # Handle different commands based on user input
        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))  # Send the HELP command to the server
        
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))  # Send the LOGOUT command to the server
            break  # Exit the loop to disconnect
        
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))  # Send the LIST command to the server
        
        # Handle the UPLOAD command (sending a file to the server)
        elif cmd == "UPLOAD":
            path = data[1]  # Get the file path from the input
            with open(f"{path}", "r") as f:  # Open the file in read mode
                text = f.read()  # Read the content of the file
            filename = path.split("/")[-1]  # Extract the filename from the path
            send_data = f"{cmd}@{filename}@{text}"  # Format the data to send (UPLOAD@filename@content)
            client.send(send_data.encode(FORMAT))  # Send the data to the server
        
        # Handle the DELETE command (deleting a file from the server)
        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))  # Send the DELETE command with the filename

    # After the loop ends, print a disconnection message
    print("Disconnected From The Server")

# Entry point of the script
if __name__ == "__main__":
    main()  # Call the main function to start the client
