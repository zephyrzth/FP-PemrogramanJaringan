from tkinter import *

window = Tk()

game_frame = Frame(window)
game_frame.pack(side="left")

playerTurn = 2
board_code = [[0 for i in range(8)] for j in range(8)]

board_code[3][3] = board_code[4][4] = 1
board_code[4][3] = board_code[3][4] = 2

def inputImage(location):
    image = PhotoImage(file=location)
    display_image = image.subsample(4, 4)
    return display_image

def setPlayer(ore_no_turn):
    playerTurn = ore_no_turn

def turn(event):

    x = event.x_root - game_frame.winfo_rootx() 
    y = event.y_root - game_frame.winfo_rooty()

    z = game_frame.grid_location(x,y)
    print( z )

    if(playerTurn == 2): setPlayer(2)
    else: setPlayer(1)


NONE_BOARD_LOCATION = "assets/none.png"
WHITE_BOARD_LOCATION = "assets/white.png"
BLACK_BOARD_LOCATION = "assets/black.png"

NONE_BOARD_IMAGE = inputImage(NONE_BOARD_LOCATION)
WHITE_BOARD_IMAGE = inputImage(WHITE_BOARD_LOCATION)
BLACK_BOARD_IMAGE = inputImage(BLACK_BOARD_LOCATION)

for i in range(8):
    for j in range(8):

        if(board_code[i][j]==0):
            label = Label(
                game_frame,  
                image=NONE_BOARD_IMAGE,
            )
            label.bind("<Button-1>",turn)
            label.grid(row=i, column=j)
        elif(board_code[i][j]==1):
            label = Label(
                game_frame,  
                image=WHITE_BOARD_IMAGE
            )
            label.grid(row=i, column=j)
        elif(board_code[i][j]==2):
            label = Label(
                game_frame,  
                image=BLACK_BOARD_IMAGE
            )
            label.grid(row=i, column=j)

window.mainloop()