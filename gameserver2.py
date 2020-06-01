import socket
import select
import sys
import threading
import struct

# Game Server Socket
gameserver_address = ('127.0.0.1', 5000)
gameserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gameserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
gameserver_socket.bind(gameserver_address)
gameserver_socket.listen(100)


def gameAccept():
    running = True
    while running:
        client_socket, client_address = gameserver_socket.accept()
        print("Game: Client " + str(client_address) + " connected.")

        ClientSocket(client_socket, client_address).start()


# gameStatus List:
# 0 exit
# 1 play: player 1 turn
# 2 play: player 2 turn
# 3 finish

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

    def run(self):
        running = True
        while running:
            try:
                print("room list: " + str(GameServer.gameServerList))
                print("player list: " + str(GameServer.allPlayerList))
                data_message = self.client_socket.recv(self.size)
                print(str(data_message.decode()))

                if str(data_message.decode()) == '[start]' and self.joinGame():
                    print(f"Room ID: {self.gameServer.getRoomId()}, Room Player: {self.gameServer.roomPlayer}")
                    while self.gameServer.gameStatus == GameServer.CODE_GAME_PREPARING:
                        self.client_socket.send(str(self.gameServer.gameStatus).encode())
                    self.client_socket.send(str(self.gameServer.gameStatus).encode())
                elif str(data_message.decode()) == '[quit]' and self.exitGame():
                    print(f"Client {self.client_address} exiting")
                    running = False
                else:
                    self.broadcast(data_message)
            except:
                break


class GameServer:  # Room Class
    gameServerList = []  # List semua room (static) : GameServer
    allPlayerList = []  # List semua pemain (static) : ClientSocket
    CODE_GAME_PREPARING = 0
    CODE_GAME_PLAYING = 1
    CODE_GAME_END = 2
    ROOM_PLAYER_LIMIT = 2

    def __init__(self):
        self.gameStatus = GameServer.CODE_GAME_PREPARING
        self.roomPlayer = []  # List pemain dalam room
        self.roomWinner = None

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

    def broadcast(self, client_object, data):
        try:
            for sock in self.roomPlayer:
                if sock != client_object:
                    sock.client_socket.send(data)
        except:
            return False

    def findColor(self, client_object):
        try:
            return self.roomPlayer.index(client_object) + 1
        except:
            return None

    def getRoomId(self):
        try:
            return GameServer.gameServerList.index(self) + 1
        except:
            return None

    def exitPlayer(self, client_object):
        try:
            self.roomPlayer.remove(client_object)
            GameServer.allPlayerList.remove(client_object)
            if len(self.roomPlayer) < 1:
                GameServer.gameServerList.remove(self)
            return True
        except:
            return False


if __name__ == '__main__':
    t1 = threading.Thread(gameAccept()).start()
    t1.join()
