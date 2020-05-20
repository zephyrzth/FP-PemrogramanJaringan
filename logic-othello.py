# array dengan value 0 brarti belum berisi
# array dengan value 1 terisi dengan bidak hitam
# array dengan value 2 terisi dengan bidak putih

class Othello:
    board = [[0 for i in range(8)] for j in range(8)]
    whitePieces = 0
    blackPieces = 0
    
    def __init__(self):
        # kondisi pertama kali permainan
        # 2 bidak putih dan 2 bidak hitam saling bersilangan di tengah
        Othello.board[4][3] = Othello.board[3][4] = 1
        Othello.board[3][3] = Othello.board[4][4] = 2
        self.turn = 1

    def countPieces(self):
        Othello.whitePieces = 0
        Othello.blackPieces = 0
        for i in range(8):
            for j in range(8):
                if(Othello.board[i][j] == 1):
                    Othello.blackPieces += 1
                elif(Othello.board[i][j] == 2):
                    Othello.whitePieces += 1

    def displayBoard(self):
        # GUI mungkin ngubah disini nantinya
        for row in Othello.board:
            print("-----------------")
            print("|", end="")
            for element in row:
                if(element == 0): 
                    print(" |", end="")
                elif(element == 1): 
                    print("B|", end="")
                else:
                    print("W|", end="")
            print("")
        print("-----------------")

    def fillBoard(self):
        # fungsi untuk ngisi bidaknya
        # Beberapa hal yang harus di cek:
        # 1. Papan masih kosong
        # 2. Papan yang dipilih memiliki pasangan diantara bidak lawan
        # Misal harus 1 2 2 2 (maka player 1 bisa naruh di samping bidak angka 2 tersebut)
        # Kalau nomor 2 sudah terpenuhi, maka semua bidak diantara 1 tersebut akan menjadi sama warnanya
        # Sebagai contoh tadi 1 2 2 2 1 maka akan berubah menjadi 1 1 1 1 1
        if self.isValidMove(int(self.positionx), int(self.positiony)):
            Othello.board[int(self.positionx)][int(self.positiony)] = self.turn
            return True
        else:
            print("\nSorry, your move violate the rules, Please try another move!\n")
            return False

    def isOnBoard(self, x, y):
        # Fungsi untuk mengecek apakah koordinat x,y berada dalam papan
        return x >= 0 and x <= 7 and y >= 0 and y <=7

    def isEmptyBoard(self, x, y):
        # Fungsi untuk mengecek apakah koordinat x,y kosong atau tidak
        return Othello.board[x][y] == 0

    def isEnemyDisk(self, x, y):
        # Fungsi untuk mengecek apakah koordinat x,y bidak lawan atau tidak
        return Othello.board[x][y] != self.turn

    def isValidMove(self, x, y):
        # Fungsi untuk mengecek apakah valid dan apakah ada bidak yang perlu dialik warnanya
        # Jika bidak yang dipilih diluar papan
        if not self.isOnBoard(int(self.positionx), int(self.positiony)):
            return False
        isValid = False
        # Jika kotak yang dipilih masih kosong   
        if self.isEmptyBoard(x, y):
            # Untuk mengecek 8 arah
            ARRAY_DIRECTION=[
                [-1 ,  0],  # Atas
                [ 1 ,  0],  # Bawah
                [ 0 ,  1],  # Kanan
                [ 0 , -1],  # Kiri
                [-1 ,  1],  # Kanan Atas
                [-1 , -1],  # Kiri Atas
                [ 1 ,  1],  # Kanan Bawah
                [ 1 , -1],  # Kiri Bawah
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
            if(isValid):
                self.updateBoard(allDisktoFlip)
        return isValid

    def updateBoard(self, diskToFlip):
        # Fungsi untuk update board
        # update koordinat board menjadi warna bidak player sekarang
        for x in diskToFlip:
            Othello.board[x[0]][x[1]] = self.turn

    def isFinished(self):
        # Fungsi untuk mengecek apakah semua board sudah terisi penuh
        for i in range(8):
            for j in range(8):
                # Jika ada kotak yang masih kosong maka belum selesai gamenya
                if Othello.board[i][j] == 0:
                    return False
        return True

    def printResult(self):
        # Fungsi untuk print hasil akhir game
        self.displayBoard()
        self.countPieces()
        print("\nBlack Pieces (Player 1): " + str(self.blackPieces))
        print("\nWhite Pieces (Player 2): " + str(self.whitePieces))
        if self.blackPieces > self.whitePieces:
            print("\nCongratulations!!! Player 1 win!\n")
        elif self.whitePieces > self.blackPieces:
            print("\nCongratulations!!! Player 2 win!\n")
        else:
            print("\nCongratulations!!! The result is draw!\n")
    
    def play(self):
        while(True):
            while(True):
                self.displayBoard()
                self.positionx=input(">>Player 1 (Black) turn, choose x coordinate: ")
                self.positiony=input(">>Player 1 (Black) turn, choose y coordinate: ")
                if self.fillBoard():
                    break            
            # print(self.isFinished)
            if self.isFinished():
                self.printResult()
                break
            self.turn = 2
            while(True):
                self.displayBoard()
                self.positionx=input(">>Player 2 (White) turn, choose x coordinate: ")
                self.positiony=input(">>Player 2 (White) turn, choose x coordinate: ")
                if self.fillBoard():
                    break
            if self.isFinished():
                self.printResult()
                break
            self.turn = 1

ot = Othello()
ot.play()