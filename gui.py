from tkinter import *

window = Tk()

def inputImage(location):
    image = PhotoImage(file=location)
    display_image = image.subsample(4, 4)
    return display_image

NONE_BOARD_LOCATION = "assets/none.png"
WHITE_BOARD_LOCATION = "assets/white.png"
BLACK_BOARD_LOCATION = "assets/black.png"

NONE_BOARD_IMAGE = inputImage(NONE_BOARD_LOCATION)
WHITE_BOARD_IMAGE = inputImage(WHITE_BOARD_LOCATION)
BLACK_BOARD_IMAGE = inputImage(BLACK_BOARD_LOCATION)

board_code = [[0 for i in range(8)] for j in range(8)]

board_code[3][3] = board_code[4][4] = 1
board_code[4][3] = board_code[3][4] = 2

game_frame = Frame(window)
game_frame.pack(side="left")

for i in range(8):
    for j in range(8):

        if(board_code[i][j]==0):
            label = Label(
                game_frame,  
                image=NONE_BOARD_IMAGE
            )
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