from tkinter import *
from socket import *
import _thread

# PART 1: Initializing server connection
def initialize_server():

    # initialize socket
    s = socket(AF_INET, SOCK_STREAM)

    # configuring the details of server
    host = 'Piyush'
    port = 23451

    # initialize server
    s.bind((host, port))

    # set no. of clients
    s.listen(1)

    # accept the connection from client
    conn, addr = s.accept()
    return conn


# PART 2: Updating the chat log
def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)

    # update the message in the window
    if state == 0:
        chatlog.insert(END, 'YOU: ' + msg)
    else:
        chatlog.insert(END, 'CHRIS: ' + msg)
    chatlog.config(state=DISABLED)



# PART3: Creating function to send & receive message
def send():
    global textbox

    # get the message
    msg = textbox.get("0.0", END)

    # update the chatlog
    update_chat(msg, 0)

    # send the message
    conn.send(msg.encode('ascii'))
    textbox.delete("0.0", END)


# Function to receive message
def receive():
    while 1:
        try:
            data = conn.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass


# PART 4: Creating GUI function
def GUI():

    global chatlog
    global textbox

    # initialize tkinter object
    gui = Tk()

    # set title for the window
    gui.title("Server (Piyush)")

    # set size for the window
    gui.geometry("380x430")

    # text space to display messages
    chatlog = Text(gui, bg='light gray')    # Setting the background colour of the display box.
    chatlog.config(state=DISABLED)          # Disabling the display text box, so that we cannot write anything in the display box.

    # button to send messages
    sendbutton = Button(gui, bg='light Green', fg='blue', text='SEND', command=send)


    # textbox to type messages
    textbox = Text(gui, bg='white')     # Creating a text box to type message, with background colour= white

    # place the components in the window
    chatlog.place(x=6, y=6, height=386, width=370)
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)

    # Using the ENTER (i.e. <KeyRelease-Return> ) key to send the message
    textbox.bind("<KeyRelease-Return>", press)

    # create thread to capture messages continuously
    # start creates a new thread
    _thread.start_new_thread(receive, ())

    # to keep the window in loop
    gui.mainloop()


# Creating press event for ENTER key
def press(event):
    send()


# Part 5: Creating the main function
if __name__ == '__main__':
    chatlog = None
    textbox = None
    conn = initialize_server()
    GUI()