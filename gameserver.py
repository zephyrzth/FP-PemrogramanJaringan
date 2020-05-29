import socket
import select
import sys
import threading

# Membuat game server socket pada port 8081
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []

# Membuat chat server socket pada port 5000
chatServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chatServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 5000
chatServer.bind((ip_address, port))
chatServer.listen(100)
list_of_chat_clients = []
print("Waiting for client.,.,.,.,.")
clientCount = 0
run = True

def clientThread(conn, addr):
    # Fungsi untuk menghandle client game thread
    global list_of_clients
    global run
    while run:
        try:
            message = conn.recv(2048).decode()
            
            if message == "[quit]":
                print('<' + addr[0] + '> left the game')
                remove(conn)
                print("a " + str(len(list_of_clients)))
                if len(list_of_clients) == 0:
                    run = False
                    print("keluar game")
                    break
                
            if message:
                print('<' + addr[0] + '>' + message)
                message_to_send = message
                broadcast(message_to_send, conn)
        except:
            continue
    server.close()

def broadcast(message, connection):
    # Fungsi untuk membroadcast koordinat bidak dalam game
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def remove(connection):
    # Fungsi untuk meremove koneksi client game
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def gameServerMain(): 
    # Fungsi untuk menghandle client yang ingin melakukan koneksi dengan server game socket
    global list_of_clients
    global clientCount
    global run
    while run:
        try:
            try:
                conn, addr = server.accept()
            except:
                break
            list_of_clients.append(conn)
            clientCount += 1
            print(addr[0] + 'connected')
            playerColor = 1
            if clientCount % 2 == 0:
                playerColor = 2
            print("Player " + str(playerColor))
            conn.send(str(playerColor).encode())
            threading.Thread(target=clientThread, args=(conn, addr)).start()
            if run == False:
                break
        except KeyboardInterrupt:
            break

def chatClientThread(conn, addr):
    # Fungsi untuk menghandle client chat thread
    global list_of_chat_clients
    global run
    while run:
        try:
            message = conn.recv(2048).decode()
            
            if message == "[quit]":
                print('<' + addr[0] + '> left the chat')
                removeChat(conn)
                print("b " + str(len(list_of_chat_clients)))
                if len(list_of_chat_clients) == 0:
                    run = False  
                    print("keluar chat")
                    break
                
            if message:
                print('<' + addr[0] + '>' + message)
                message_to_send = '<' + 'opponent' + '>' + message
                broadcastChat(message_to_send, conn)
                
        except:
            continue
    chatServer.close()

def broadcastChat(message, connection):
    # Fungsi untuk membroadcast chat
    for clients in list_of_chat_clients:
        if clients!=connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                removeChat(clients)

def removeChat(connection):
    # Fungsi untuk meremove koneksi client chat
    if connection in list_of_chat_clients:
        list_of_chat_clients.remove(connection)

def chatServerMain(): 
    # Fungsi untuk menghandle client yang ingin melakukan koneksi dengan server chat socket
    while run:
        try:
            try:
                conn, addr = chatServer.accept()
            except:
                break
            list_of_chat_clients.append(conn)
            print(addr[0] + 'chat connected')
            threading.Thread(target=chatClientThread, args=(conn, addr)).start()
            if run == False:
                break
        except KeyboardInterrupt:
            break

# Membuat thread untuk menghandle client bagian game dan chat
threading.Thread(target=gameServerMain).start()
threading.Thread(target=chatServerMain).start()