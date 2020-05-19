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
                    Othello.whitePieces += 1
                elif(Othello.board[i][j] == 2):
                    Othello.blackPieces += 1

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
        if self.checkBoard():
            Othello.board[int(self.positionx)][int(self.positiony)] = self.turn
        else:
            print("\nSorry, your move violate the rules\n")

    def isOnBoard(self, x, y):
        # Fungsi untuk mengecek apakah koordinat x,y berada dalam papan
        return x >= 0 and x <= 7 and y >= 0 and y <=7

    def checkBoard(self):
        # Fungsi untuk mengecek apakah valid dan apakah ada bidak yang perlu dialik warnanya
        # Jika bidak yang dipilih diluar papan
        if not self.isOnBoard(int(self.positionx), int(self.positiony)):
            return False
        # Jika papan yang dipilih masih kosong
        if Othello.board[int(self.positionx)][int(self.positiony)] == 0:
            isValid = 0
            # Mengecek bagian atas
            diskToFlip = []
            for x in range(int(self.positionx)-1, -1, -1):
                # Cek apakah ada bidak ditetangganya
                if Othello.board[x][int(self.positiony)] == 0:
                    break
                # Cek apakah menemukan bidak yang sama
                elif Othello.board[x][int(self.positiony)] == self.turn:
                    if diskToFlip:
                        isValid = 1
                        self.updateBoard(diskToFlip)
                    break
                else:
                    # masukkan koordinat dari potensi bidak yang mungkin diganti warna
                    diskToFlip.append([x, int(self.positiony)])
            # Mengecek bagian bawah
            diskToFlip = []
            for x in range(int(self.positionx)+1, 8):
                # Cek apakah ada bidak ditetangganya
                if Othello.board[x][int(self.positiony)] == 0:
                    break
                # Cek apakah menemukan bidak yang sama
                elif Othello.board[x][int(self.positiony)] == self.turn:
                    if diskToFlip:
                        isValid = 1
                        self.updateBoard(diskToFlip)
                    break
                else:
                    # masukkan koordinat dari potensi bidak yang mungkin diganti warna
                    diskToFlip.append([x, int(self.positiony)])
            # Mengecek bagian kiri
            diskToFlip = []
            for x in range(int(self.positiony)-1, -1, -1):
                # Cek apakah ada bidak ditetangganya
                if Othello.board[int(self.positionx)][x] == 0:
                    break
                # Cek apakah menemukan bidak yang sama
                elif Othello.board[int(self.positionx)][x] == self.turn:
                    if diskToFlip:
                        isValid = 1
                        self.updateBoard(diskToFlip)
                    break
                else:
                    # masukkan koordinat dari potensi bidak yang mungkin diganti warna
                    diskToFlip.append([int(self.positionx), x])
            # Mengecek bagian kanan
            diskToFlip = []
            for x in range(int(self.positiony)+1, 8):
                # Cek apakah ada bidak ditetangganya
                if Othello.board[int(self.positionx)][x] == 0:
                    break
                # Cek apakah menemukan bidak yang sama
                elif Othello.board[int(self.positionx)][x] == self.turn:
                    if diskToFlip:
                        isValid = 1
                        self.updateBoard(diskToFlip)
                    break
                else:
                    # masukkan koordinat dari potensi bidak yang mungkin diganti warna
                    diskToFlip.append([int(self.positionx), x])
            # Mengecek bagian diagonal kiri atas
            diskToFlip = []
            diagonalBoundary = min(int(self.positionx), int(self.positiony))
            for x in range(1, diagonalBoundary+1):
                # Cek apakah ada bidak ditetangganya
                if Othello.board[int(self.positionx)-x][int(self.positiony)-x] == 0:
                    break
                # Cek apakah menemukan bidak yang sama
                elif Othello.board[int(self.positionx)-x][int(self.positiony)-x] == self.turn:
                    if diskToFlip:
                        isValid = 1
                        self.updateBoard(diskToFlip)
                    break
                else:
                    # masukkan koordinat dari potensi bidak yang mungkin diganti warna
                    diskToFlip.append([int(self.positionx)-x, int(self.positiony)-x])
            # Mengecek bagian diagonal kanan bawah
            diskToFlip = []
            diagonalBoundary = 7 - max(int(self.positionx), int(self.positiony))
            for x in range(1, diagonalBoundary+1):
                # Cek apakah ada bidak ditetangganya
                if Othello.board[int(self.positionx)+x][int(self.positiony)+x] == 0:
                    break
                # Cek apakah menemukan bidak yang sama
                elif Othello.board[int(self.positionx)+x][int(self.positiony)+x] == self.turn:
                    if diskToFlip:
                        isValid = 1
                        self.updateBoard(diskToFlip)
                    break
                else:
                    # masukkan koordinat dari potensi bidak yang mungkin diganti warna
                    diskToFlip.append([int(self.positionx)+x, int(self.positiony)+x])
            # Mengecek bagian diagonal kanan atas
            diskToFlip = []
            for x in range(1, 8):
                # Cek apakah ada bidak ditetangganya dan apakah masih dalam boundary
                if Othello.board[int(self.positionx)-x][int(self.positiony)+x] == 0 or not self.isOnBoard(int(self.positionx)-x, int(self.positiony)+x):
                    break
                # Cek apakah menemukan bidak yang sama
                elif Othello.board[int(self.positionx)-x][int(self.positiony)+x] == self.turn:
                    if diskToFlip:
                        isValid = 1
                        self.updateBoard(diskToFlip)
                    break
                else:
                    # masukkan koordinat dari potensi bidak yang mungkin diganti warna
                    diskToFlip.append([int(self.positionx)-x, int(self.positiony)+x])
            # Mengecek bagian diagonal kiri bawah
            diskToFlip = []
            for x in range(1, 8):
                # Cek apakah ada bidak ditetangganya dan apakah masih dalam boudnary
                if Othello.board[int(self.positionx)+x][int(self.positiony)-x] == 0 or not self.isOnBoard(int(self.positionx)+x, int(self.positiony)-x):
                    break
                # Cek apakah menemukan bidak yang sama
                elif Othello.board[int(self.positionx)+x][int(self.positiony)-x] == self.turn:
                    if diskToFlip:
                        isValid = 1
                        self.updateBoard(diskToFlip)
                    break
                else:
                    # masukkan koordinat dari potensi bidak yang mungkin diganti warna
                    diskToFlip.append([int(self.positionx)+x, int(self.positiony)-x])
            if isValid == 1:
                return True
            else:
                return False
        else:
            return False  

    def updateBoard(self, diskToFlip):
        # Fungsi untuk update board
        print("update board")
        # update koordinat board menjadi warna bidak player sekarang
        for x in diskToFlip:
            Othello.board[x[0]][x[1]] = self.turn
    
    def play(self):
        while(True):
            self.displayBoard()
            self.positionx=input(">>Player 1 turn, choose x coordinate: ")
            self.positiony=input(">>Player 1 turn, choose y coordinate: ")
            self.fillBoard()
            self.displayBoard()
            self.turn = 2
            self.positionx=input(">>Player 2 turn, choose x coordinate: ")
            self.positiony=input(">>Player 2 turn, choose x coordinate: ")
            self.fillBoard()
            self.turn = 1

ot = Othello()
ot.play()