import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
import socket
import threading
import time

# root window
root = tk.Tk()
root.geometry('720x480')
root.title('InfoProc')

# create a tab
tab = ttk.Notebook(root)
tab.pack(pady=10, expand=True)

# create frames
gameSelection = ttk.Frame(tab, width=720, height=480)
settings = ttk.Frame(tab, width=720, height=480)

gameSelection.pack(fill='both', expand=True)
settings.pack(fill='both', expand=True)

# add frames to tabs
tab.add(gameSelection, text='Game Selection')
tab.add(settings, text='Settings')

# create game buttons
buttonFont = font.Font(family='Arial', weight="bold", size=8)

# these buttons have been added to 'gameSelection tab'
Button(gameSelection, text="Game 1", height="32", width="32", bg='red', fg='white', font=buttonFont).pack(padx=5,
                                                                                                          pady=15,
                                                                                                          side=tk.LEFT)
Button(gameSelection, text="Game 2", height="32", width="32", bg='green', fg='white', font=buttonFont).pack(padx=5,
                                                                                                            pady=15,
                                                                                                            side=tk.LEFT)
Button(gameSelection, text="Game 3", height="32", width="32", bg='blue', fg='white', font=buttonFont).pack(padx=5,
                                                                                                           pady=15,
                                                                                                           side=tk.LEFT)


# number checking
def only_numbers(char):
    if char.isdigit():
        return True
    elif char == ".":
        return True
    else:
        return False


validation = settings.register(only_numbers)

def changeText():
    TCPValues.config(text="TCP Set: " + ipAddressEntry.get() + ":" + portEntry.get())

def setLocalHost():
    global chkValue
    if chkValue == 0:
        ipVar.set("localhost")
        chkValue = 1
    else:
        chkValue = 0
        ipVar.set("")

def cycleTCP (client_socket) : 
    answer = ' '
    player = ' '
    sequence = ' '

    while True : 
        if client_socket.recv(1024).decode == 'end' :
            break
        player = client_socket.recv(1024).decode()
        sequence = client_socket.recv(1024).decode()
    client_socket.close()
    
    

def startTCP():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ipAddressEntry.get(), int(portEntry.get())))
        print('Connected to server')
        TCPError.configure(fg="green", text="Connected")
        status.configure(bg="green")
    except:
        TCPError.configure(fg="red", text="Failed to Connect")
        status.configure(bg="red")

    x = threading.Thread(target=cycleTCP, args=(client_socket,), daemon=True)
    return client_socket

chkValue = tk.BooleanVar()
chkValue = False

TCPTitle = Label(settings, text="Enter IP & Port")
TCPTitle.place(x=20.0, y=10.0)

TCPError = Label(settings, text="", fg="red")
TCPError.place(x=250.0, y=162.0)

ipVar = tk.StringVar()
ipName = Label(settings, text="IP")
ipName.place(x=20.0, y=40.0)
ipAddressEntry = Entry(settings, textvariable=ipVar, validate="key", validatecommand=(validation, '%S'))
ipAddressEntry.place(x=80.0, y=40.0)

localhost = Checkbutton(settings, text = "localhost", command=setLocalHost, var=chkValue)
localhost.place(x=220.0, y=38.0)

portVar = tk.StringVar()
portName = Label(settings, text="Port")
portName.place(x=20.0, y=80.0)
portEntry = Entry(settings, textvariable=portVar, validate="key", validatecommand=(validation, '%S'))
portEntry.place(x=80.0, y=80.0)

TCPValues = Label(settings, text="TCP Set: 0.0.0.0: 00000")
TCPValues.place(x=20.0, y=200.0)

saveButton = Button(settings, text="Save", command=changeText, height="1", width="25")
saveButton.place(x=20.0, y=120.0)

connectButton = Button(settings, text="CONNECT", command=startTCP, height="1", width="25")
connectButton.place(x=20.0, y=160.0)

status = Button(settings, bg='red', width="2", state=DISABLED)
status.place(x=220.0, y=160.0)

client_socket = startTCP()


# use ipAddressEntry.get() & portEntry.get() to get TCP things
root.mainloop()
