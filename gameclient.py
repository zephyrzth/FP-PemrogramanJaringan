import socket
import select
import sys
import msvcrt
from threading import Thread
from tkinter import *

# array dengan value 0 brarti belum berisi
# array dengan value 1 terisi dengan bidak hitam
# array dengan value 2 terisi dengan bidak putih

class Othello:
    board = [[0 for i in range(8)] for j in range(8)]
    # Variabel untuk menghitung jumlah player yang gabisa gerak
    cantMove = 0

    def __init__(self, playerColor):
        # kondisi pertama kali permainan
        # 2 bidak putih dan 2 bidak hitam saling bersilangan di tengah
        self.board[4][3] = self.board[3][4] = 1
        self.board[3][3] = self.board[4][4] = 2
        print(playerColor)
        self.myTurn = playerColor
        self.turn = 1

    def countPieces(self):
        whitePieces = 0
        blackPieces = 0
        for i in range(8):
            for j in range(8):
                if(self.board[i][j] == 1):
                    blackPieces += 1
                elif(self.board[i][j] == 2):
                    whitePieces += 1
        
        return [blackPieces, whitePieces]

    def isOnBoard(self, x, y):
        # Fungsi untuk mengecek apakah koordinat x,y berada dalam papan
        return x >= 0 and x <= 7 and y >= 0 and y <=7

    def isEmptyBoard(self, x, y):
        # Fungsi untuk mengecek apakah koordinat x,y kosong atau tidak
        return self.board[x][y] == 0

    def isEnemyDisk(self, x, y):
        # Fungsi untuk mengecek apakah koordinat x,y bidak lawan atau tidak
        return self.board[x][y] != self.turn

    def isValidMove(self, x, y, isClicked):
        # Fungsi untuk mengecek apakah valid dan apakah ada bidak yang perlu dialik warnanya
        # Jika bidak yang dipilih diluar papan
        if not self.isOnBoard(x, y):
            return False
        isValid = False
        # Jika kotak yang dipilih masih kosong   
        if self.isEmptyBoard(x, y):
            # Untuk mengecek 8 arah
            ARRAY_DIRECTION=[
                [-1 ,  0],  # Kiri
                [ 1 ,  0],  # Kanan
                [ 0 ,  1],  # Bawah
                [ 0 , -1],  # Atas
                [-1 ,  1],  # Kiri Bawah
                [-1 , -1],  # Kiri Atas
                [ 1 ,  1],  # Kanan Bawah
                [ 1 , -1],  # Kanan Atas
            ]
            allDisktoFlip = []

            for direction in ARRAY_DIRECTION:

                disktoflip = []
                iter_x = x+direction[0]
                iter_y = y+direction[1]
                # Lakukan looping selama pengecekan masih berada di dalam border
                while self.isOnBoard(iter_x, iter_y):
                    # Jika papan yang dipilih masih kosong
                    if self.isEmptyBoard(iter_x, iter_y):
                        break
                    # Cek apakah bidak tetangganya adalah lawan
                    elif(self.isEnemyDisk(iter_x, iter_y)):
                        disktoflip.append([iter_x, iter_y])
                    else:
                        if(disktoflip):
                            isValid = True
                            for diskPos in disktoflip:
                                allDisktoFlip.append(diskPos)
                        break
                    iter_x += direction[0]
                    iter_y += direction[1]
            if(isValid & isClicked):
                self.updateBoard(allDisktoFlip)
        return isValid

    def updateBoard(self, diskToFlip):
        # Fungsi untuk update board
        # update koordinat board menjadi warna bidak player sekarang
        for x in diskToFlip:
            self.board[x[0]][x[1]] = self.turn

    def isFinished(self):
        # Fungsi untuk mengecek apakah game sudah selesai
        isFull = True
        for i in range(8):
            for j in range(8):
                # Jika ada kotak yang masih kosong maka belum selesai gamenya
                if self.board[i][j] == 0:
                    # Jika player masih bisa melakukan sebuah move pada suatu turn maka belum selesai gamenya
                    if self.isValidMove(i, j, False):
                        self.cantMove = 0              
                        return False
                    isFull = False
        # Jika board sudah penuh dengan bidak
        if isFull:
            return True
        else:
            self.cantMove += 1
            # Jika kedua player tidak bisa bergerak
            if self.cantMove == 2:
                return True
            else:
                return False

class App:
    NONE_BOARD_LOCATION = "assets/none.png"
    WHITE_BOARD_LOCATION = "assets/white.png"
    BLACK_BOARD_LOCATION = "assets/black.png"
    HELPER_BOARD_LOCATION = "assets/helper.png"

    def __init__(self):
        self.windows = Tk()
        self.loadImage()
        self.generate_socket()
        playerColor = self.server.recv(2048).decode()
        self.othello = Othello(int(playerColor))
        self.makeGameFrame()
        self.listen_thread()
        self.windows.mainloop()

    def generate_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip_address = '127.0.0.1'
        port = 8081
        self.server.connect((ip_address, port))

    def listen_thread(self):
        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def receive(self):
        msg = 1
        print("do space every want chat\n[quit]for exit")

        while True:
            try:
                sockets_list = [self.server]
                read_socket, write_socket, error_socket = select.select(sockets_list, [], [],1)
                
                # if msvcrt.kbhit():
                #   read_socket.append(sys.stdin)
                # if msvcrt.kbhit():
                #     read_socket.append(sys.stdin)
                    # key = msvcrt.getche()
                    # if str(key) == "b'q'": # Enter key
                    #   break
                for socks in read_socket:
                    if socks == self.server:
                        message = socks.recv(2048).decode()
                        opponentCoordinate = eval(message[10:])
                        print(opponentCoordinate)
                        if(self.othello.isValidMove(opponentCoordinate[0], opponentCoordinate[1], True)):
                            self.othello.board[opponentCoordinate[0]][opponentCoordinate[1]] = self.othello.turn
                            if(self.othello.turn == 2): self.setPlayer(1)
                            else: self.setPlayer(2)
                            self.displayBoard()
                            self.makeScoreBoard()
                        print(self.othello.cantMove)
                        if self.othello.cantMove != 0:
                            if(self.othello.turn == 2): self.setPlayer(1)
                            else: self.setPlayer(2)
                            self.displayBoard()
                            self.makeScoreBoard()
                        # self.msg_list.insert(END, message)
                    else:                        
                        if message == "[quit]": # Enter key
                            msg = 0
                            # self.msg_list.insert(END, "please exit the chatbox using button exit")
                            #self.on_close()
                        # else:
                            # self.msg_list.insert(END, "<You> " + message)
                            # self.server.send(message.encode())
                            
                        sys.stdout.flush()
                
                if msg == 0:
                    self.server.send(message.encode())
                    break
            except OSError:  # Possibly client has left the chat.
                break
        self.server.close()
    
    def loadImage(self):
        self.NONE_BOARD_IMAGE   = self.inputImage(self.NONE_BOARD_LOCATION)
        self.WHITE_BOARD_IMAGE  = self.inputImage(self.WHITE_BOARD_LOCATION)
        self.BLACK_BOARD_IMAGE  = self.inputImage(self.BLACK_BOARD_LOCATION)
        self.HELPER_BOARD_IMAGE = self.inputImage(self.HELPER_BOARD_LOCATION)

    def inputImage(self, location):
        image = PhotoImage(file=location)
        display_image = image.subsample(4, 4)
        return display_image

    def makeGameFrame(self):
        self.game_frame = Frame(self.windows)
        self.game_frame.pack(side="left")
        self.winNotification = Frame(self.game_frame)
        self.winNotification.pack(side="top")
        self.board_frame = Frame(self.game_frame)
        self.board_frame.pack(side="top")
        self.score_frame = Frame(self.game_frame)
        self.score_frame.pack(side="top")
        self.playerDescription = Frame(self.game_frame)
        self.playerDescription.pack(side="top")

        self.displayBoard()
        self.makeScoreBoard()

    def displayBoard(self):
        for i in range(8):
            for j in range(8):
                if(self.othello.board[i][j]==0):
                    label = Label(
                        self.board_frame,  
                        image=self.NONE_BOARD_IMAGE,
                    )
                    label.bind("<Enter>", self.hover)
                    label.grid(column=i, row=j)
                elif(self.othello.board[i][j]==2):
                    label = Label(
                        self.board_frame,  
                        image=self.WHITE_BOARD_IMAGE
                    )
                    label.grid(column=i, row=j)
                    label.bind("<Enter>", self.out)
                elif(self.othello.board[i][j]==1):
                    label = Label(
                        self.board_frame,  
                        image=self.BLACK_BOARD_IMAGE
                    )
                    label.grid(column=i, row=j)
                    label.bind("<Enter>", self.out)
        self.helperLabel = Label(self.board_frame)
        self.helperLabel.bind("<Button-1>", self.turn)
    
    def makeScoreBoard(self):
        score = self.othello.countPieces()
        playerName1_label = Label(
                                self.score_frame, 
                                text="Player 1", 
                                font=("Arial", 18), 
                                fg="white", 
                                bg="black", 
                                width=8
                            )
        playerScore1_label = Label(
                                self.score_frame, 
                                text=str(score[0]), 
                                font=("Arial", 18), 
                                fg="white", 
                                bg="black", 
                                width=4
                            )
        playerName2_label = Label(
                                self.score_frame, 
                                text="Player 2", 
                                font=("Arial", 18), 
                                fg="black", 
                                bg="white", 
                                width=8
                            )
        playerScore2_label = Label(
                                self.score_frame, 
                                text=str(score[1]), 
                                font=("Arial", 18), 
                                fg="black", 
                                bg="white", 
                                width=4
                            )

        turnDescription_label = Label(
                                self.score_frame, 
                                font=("Arial", 18), 
                                width=12
                            )

        winNotification_label = Label(
                                self.winNotification, 
                                font=("Arial", 18), 
                                width=38,
                                bg="green"
                            )

        playerDescription_label = Label(
                                self.playerDescription, 
                                font=("Arial", 18), 
                                width=38,
                                bg="green"
                            )

        if(self.othello.myTurn == 1):
            playerDescription_label.configure(
                                            text="You're Player 1", 
                                            fg="black", 
                                            bg="green"
                                        )
        else:
            playerDescription_label.configure(
                                            text="You're Player 2", 
                                            fg="white", 
                                            bg="green"
                                        )

        if(self.othello.isFinished()):
            if(score[0] > score[1]):
                winNotification_label.configure(
                                                text="Player 1 Win", 
                                                fg="black", 
                                                bg="green"
                                            )
            elif(score[0] < score[1]):
                winNotification_label.configure(
                                                text="Player 2 Win", 
                                                fg="white", 
                                                bg="green"
                                            )
            else:
                winNotification_label.configure(
                                                text="Draw", 
                                                fg="black", 
                                                bg="green"
                                            )

        if(self.othello.turn==1):
            turnDescription_label.configure(
                                            text="Black's Turn", 
                                            fg="black", 
                                            bg="green"
                                        )
        else:
            turnDescription_label.configure(
                                            text="White's Turn", 
                                            fg="white", 
                                            bg="green"
                                        )

        playerName1_label.grid(row=0, column=0)
        playerScore1_label.grid(row=0, column=1)
        turnDescription_label.grid(row=0, column=4)
        playerName2_label.grid(row=0, column=7)
        playerScore2_label.grid(row=0, column=6)
        playerDescription_label.grid(row=0)
        winNotification_label.grid(row=0)

    def setPlayer(self, ore_no_turn):
        self.othello.turn = ore_no_turn

    def turn(self, event):
    
        x = event.x_root - self.board_frame.winfo_rootx() 
        y = event.y_root - self.board_frame.winfo_rooty()

        z = self.board_frame.grid_location(x,y)
        print(z)
        if self.othello.myTurn == self.othello.turn:
            if(self.othello.isValidMove(z[0], z[1], True)):
                self.othello.board[z[0]][z[1]] = self.othello.turn
                send_message = str(z)
                self.server.send(send_message.encode())
                if(self.othello.turn == 2): self.setPlayer(1)
                else: self.setPlayer(2)
                self.displayBoard()
                self.makeScoreBoard()
            print(self.othello.cantMove)
            if self.othello.cantMove != 0:
                if(self.othello.turn == 2): self.setPlayer(1)
                else: self.setPlayer(2)
                self.displayBoard()
                self.makeScoreBoard()

    def hover(self, event):
        
        x = event.x_root - self.board_frame.winfo_rootx() 
        y = event.y_root - self.board_frame.winfo_rooty()

        z = self.board_frame.grid_location(x,y)
        if self.othello.myTurn == self.othello.turn:            
            if(self.othello.isValidMove(z[0], z[1], FALSE)):
                self.helperLabel.configure(image=self.HELPER_BOARD_IMAGE)
                self.helperLabel.grid(column=z[0], row=z[1])
            else:
                self.helperLabel.configure(image=self.NONE_BOARD_IMAGE)

    def out(self, event):
        self.helperLabel.configure(image=self.NONE_BOARD_IMAGE)

myApp = App()