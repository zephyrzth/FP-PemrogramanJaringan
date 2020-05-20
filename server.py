import socket
import select
import sys

server_address = ('127.0.0.1', 5678)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

gameID = 0
# gameStatus List:
# 0 exit
# 1 play: player 1 turn
# 2 play: player 2 turn
# 3 finish

class Game:
    def __init__(self, gameID, player1, player2):
        self.gameID = gameID
        self.gameStatus = 1
        self.player1 = player1
        self.player2 = player2




try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                gameID += 1
                print(gameID)
            else:
                data = sock.recv(1024).decode()
                print(str(sock.getpeername()), str(data))
                if str(data):
                    client_socket.send(data.encode())
                else:
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit()