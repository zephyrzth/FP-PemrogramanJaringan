# array dengan value 0 brarti belum berisi
# array dengan value 1 terisi dengan bidak putih
# array dengan value 2 terisi dengan bidak hitam

class Othello:
    board = [[0 for i in range(8)] for j in range(8)]

    def __init__(self):
        # kondisi pertama kali permainan
        # 2 bidak putih dan 2 bidak hitam saling bersilangan di tengah
        Othello.board[3][3] = Othello.board[4][4] = 1
        Othello.board[4][3] = Othello.board[3][4] = 2
        self.turn = 1

    def displayBoard(self):
        # GUI mungkin ngubah disini nantinya
        for row in Othello.board:
            print("-----------------")
            print("|", end="")
            for element in row:
                if(element == 0): 
                    print(" |", end="")
                elif(element == 1): 
                    print("W|", end="")
                else:
                    print("B|", end="")
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

        Othello.board[int(self.positionx)][int(self.positiony)] = self.turn;
    
    def play(self):
        while(True):
            self.positionx=input(">>Player 1 turn, choose x coordinate: ")
            self.positiony=input(">>Player 1 turn, choose y coordinate: ")
            self.fillBoard()
            self.displayBoard()
            self.turn = 2
            self.positionx=input(">>Player 2 turn, choose x coordinate: ")
            self.positiony=input(">>Player 2 turn, choose x coordinate: ")
            self.fillBoard()
            self.displayBoard()
            self.turn = 1

ot = Othello()
ot.play()