import socket
import select
import sys
import threading
import struct
import time

# Game Server Socket
gameserver_address = ('127.0.0.1', 5000)
gameserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gameserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
gameserver_socket.bind(gameserver_address)
gameserver_socket.listen(100)


# Thread untuk accept connection
def gameAccept():
    running = True
    while running:
        client_socket, client_address = gameserver_socket.accept()
        print("Game: Client " + str(client_address) + " connected.")

        ClientSocket(client_socket, client_address).start()


# Class Client Socket untuk menghandle socket dari client
class ClientSocket(threading.Thread):
    BUFFER_SIZE = 2048
    HEADER_LENGTH = 10

    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client_socket = client
        self.client_address = address
        self.size = ClientSocket.BUFFER_SIZE
        self.gameServer = None
        self.gameColor = None

    def joinGame(self):
        self.gameServer = GameServer.join(self)
        self.gameColor = self.gameServer.findColor(self)
        print(f"Player {self.client_address} color: {self.gameColor}")
        if self.gameServer is not None and self.gameColor is not None:
            self.client_socket.send(str(self.gameColor).encode())
            return True
        return False

    def broadcast(self, data):
        return True if self.gameServer.broadcast(self, data) else False

    def exitGame(self):
        if self.gameServer.exitPlayer(self):
            self.gameServer = None
            return True
        return False

    def exitAll(self):
        if self.gameServer.exitAll():
            return True
        return False

    def run(self):
        running = True
        while running:
            try:
                print("room list: " + str(GameServer.gameServerList))
                print("player list: " + str(GameServer.allPlayerList))
                data_message = self.client_socket.recv(self.size)
                print(str(data_message.decode()))

                # Ketika client klik start game
                if str(data_message.decode()) == '[start]' and self.joinGame():
                    print(f"Room ID: {self.gameServer.getRoomId()}, Room Player: {self.gameServer.roomPlayer}")
                    while self.gameServer.gameStatus == GameServer.CODE_GAME_PREPARING:
                        self.client_socket.send(str(self.gameServer.gameStatus).encode())
                        time.sleep(2)
                    time.sleep(2)
                    self.client_socket.send(str(self.gameServer.gameStatus).encode())
                # Ketika client quit game (close / play again)
                elif str(data_message.decode()) == '[quit]':
                    self.broadcast(data_message)
                    print(f"Client {self.client_address} exiting")
                    self.exitAll()
                    print("room list: " + str(GameServer.gameServerList))
                    print("player list: " + str(GameServer.allPlayerList))
                    running = False
                # Ketika bukan keduanya akan dibroadcast
                else:
                    self.broadcast(data_message)
            except:
                break


class GameServer:  # Class untuk room game
    gameServerList = []  # List semua room (static) : GameServer
    allPlayerList = []  # List semua pemain (static) : ClientSocket
    CODE_GAME_PREPARING = 0
    CODE_GAME_PLAYING = 1
    CODE_GAME_END = 2
    ROOM_PLAYER_LIMIT = 2  # Membatasi jumlah pemain saat Join Baru

    def __init__(self):
        self.gameStatus = GameServer.CODE_GAME_PREPARING
        self.roomPlayer = []  # List pemain dalam room
        self.roomWinner = None

    # Fungsi static untuk join client object baru ke dalam room
    @staticmethod
    def join(client_object):
        try:
            notFound = True
            roomFound = None
            for i in GameServer.gameServerList:
                if len(i.roomPlayer) < GameServer.ROOM_PLAYER_LIMIT:
                    i.roomPlayer.append(client_object)
                    i.gameStatus = GameServer.CODE_GAME_PLAYING
                    roomFound = i
                    notFound = False
                    break
            if notFound:
                newGameServer = GameServer()
                newGameServer.roomPlayer.append(client_object)
                GameServer.gameServerList.append(newGameServer)
                roomFound = newGameServer

            GameServer.allPlayerList.append(client_object)
            return roomFound
        except:
            return None

    # Membroadcast ke client lain di dalam room
    def broadcast(self, client_object, data):
        try:
            for sock in self.roomPlayer:
                if sock != client_object:
                    sock.client_socket.send(data)
        except:
            return False

    # Mendapatkan flag player 1 atau player 2
    def findColor(self, client_object):
        try:
            return self.roomPlayer.index(client_object) + 1
        except:
            return None

    # Mendapatkan ID Room dari posisi room ini di list semua room
    def getRoomId(self):
        try:
            return GameServer.gameServerList.index(self) + 1
        except:
            return None

    # Handle saat player quit
    def exitPlayer(self, client_object):
        try:
            self.roomPlayer.remove(client_object)
            GameServer.allPlayerList.remove(client_object)
            if len(self.roomPlayer) < 1:
                GameServer.gameServerList.remove(self)
            return True
        except:
            return False

    # Handle untuk semua player quit
    def exitAll(self):
        try:
            for i in self.roomPlayer:
                self.exitPlayer(i)
            return True
        except:
            return False


if __name__ == '__main__':
    t1 = threading.Thread(gameAccept()).start()
    t1.join()
