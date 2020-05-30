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

# Chat Socket
chatserver_address = ('127.0.0.1', 5001)
chatserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chatserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
chatserver_socket.bind(chatserver_address)
chatserver_socket.listen(100)


def gameAccept():
    running = True
    while running:
        client_socket, client_address = gameserver_socket.accept()
        print("Game: Client " + str(client_address) + " connected.")

        ClientSocket(client_socket, client_address).start()


def chatAccept():
    running = True
    while running:
        client_socket, client_address = chatserver_socket.accept()
        print("Chat: Client " + str(client_address) + " connected.")


# gameStatus List:
# 0 exit
# 1 play: player 1 turn
# 2 play: player 2 turn
# 3 finish

class ClientSocket(threading.Thread):
    BUFFER_SIZE = 2048

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
                    print(self.gameServer.roomPlayer)
                elif str(data_message.decode()) == '[quit]' and self.exitGame():
                    print("Client keluar")
            except:
                self.exitGame()
                break


class GameServer:  # Room Class
    gameServerList = []  # Menyimpan list semua room (GameServer)
    allPlayerList = []
    CODE_GAME_PREPARING = 0
    CODE_GAME_PLAYING = 1
    CODE_GAME_END = 2
    ROOM_PLAYER_LIMIT = 2

    def __init__(self):
        self.gameMap = None
        self.gameStatus = GameServer.CODE_GAME_PREPARING
        self.roomPlayer = []
        self.roomWinner = None
        self.turnNow = 0
        self.N = 8

    @staticmethod
    def join(client_object):
        try:
            notFound = True
            roomFound = None
            for i in GameServer.gameServerList:
                if len(i.roomPlayer) < GameServer.ROOM_PLAYER_LIMIT:
                    i.roomPlayer.append(client_object)
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

    def findColor(self, client_object):
        try:
            return self.roomPlayer.index(client_object) + 1
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
    t2 = threading.Thread(chatAccept()).start()

    t1.join()
    t2.join()
