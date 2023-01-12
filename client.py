import PySimpleGUI as sg
import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect(("localhost", 12345))

# Create the GUI layout
layout = [[sg.Text("Enter your username:")],
          [sg.InputText(key="username")],
          [sg.Button("Send Username"), sg.Exit()],
          [sg.Text("Enter the username of the client you want to chat with:")],
          [sg.InputText(key="target_username")],
          [sg.Button("Send Target Username"), sg.Exit()],
          [sg.Text("Chat History:", key="history"), sg.Multiline(key="conversation", size=(40, 15))],
          [sg.Input(key="message"), sg.Button("Send Message")]
         ]

# Create the window
window = sg.Window("Chat Client", layout)

while True:
    event, values = window.Read(timeout=500)
    if event == "Send Username":
        # Send the username to the server
        s.send(values["username"].encode())
        # Receive message if the provided username already taken or not
        while "taken" in s.recv(1024).decode():
            # Update the prompt with error message
            window.FindElement("username").Update("That username is already taken. Enter a different username:")
            event, values = window.Read()
            s.send(values["username"].encode())
    elif event == "Send Target Username":
        # Send the target client's username to the server
        s.send(values["target_username"].encode())
    elif event == "Send Message":
        # Send the message to the server
        s.send(values["message"].encode())
        window.FindElement("conversation").Update(window.FindElement("conversation").Get() + '\n' + values["message"])
    elif event == "__TIMEOUT__":
        s.settimeout(0.5)
        try:
            # Receive the message from the server
            message = s.recv(1024).decode()
            # Update the conversation Text element with the message
            window.FindElement("conversation").Update(window.FindElement("conversation").Get() + '\n' + message)
        except (socket.error, socket.timeout):
            pass
    elif event == "Exit":
        break

# Close the socket and the window
s.close()
window.Close()
