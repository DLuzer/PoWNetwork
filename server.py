import socket
import sys
import threading
import os
from random import choice
from string import ascii_letters

global cond_var
global curr_count
global base
global connections

curr_count = -1
base = "Hello World!"
#True = locked, False = unlocked
cond_var = False
connections = {}


def randString(length):
	return(''.join(choice(ascii_letters) for i in range(length)))

def send_work(conn, addr):
    global curr_count
    global base
    global cond_var
    global connections


    while True:
        print(connections)
        if (cond_var == False):
            cond_var = True
            message = str(curr_count + 1) + '-' + str(curr_count + 1000000) + '-' + '6' + '-' + base
            curr_count += 1000000
            print(curr_count)

            print("sent:", message)
            conn.send(message.encode('utf-8'))
            cond_var = False

            client_in = str(conn.recv(1024))
            print("received:", client_in, "from:", addr)

            if client_in[2:6] != "done":
                print(">>>" + client_in.split(" ")[0])
                break
            else:
                hps = client_in.split(" ")[1]
                connections[addr[0]] = hps

    return 0


def main():
    global connections

    soc = socket.socket()
    host = "0.0.0.0"
    port = 6500
    soc.bind((host,port))

    thread_list = []
    soc.listen()
    input("Press enter to distribute work to all connected clients.")
    while True:
        connection, address = soc.accept()

        print(address, "connected to server")

        thread = threading.Thread(target = send_work, args = (connection, address))
        thread_list.append(thread)
        thread.start()

main()
