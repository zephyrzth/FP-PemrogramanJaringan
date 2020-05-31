from tkinter import *

class Menu:

    def __init__(self, master):
        self.root = master    
        self.button_inputname = None
        self.button_exit = None
        self.generate_gui()

    def generate_gui(self):
        namalabel = Label(self.root, text = "")
        namalabel.pack()
        self.topframe = Frame(self.root)
        self.topframe.pack()
        self.bottomframe = Frame(self.root)
        self.bottomframe.pack(side = TOP)
        
        self.button_inputname = Button(self.bottomframe, text = "Finding Match ", fg= "black",command = self.printpesan)
        self.button_inputname.pack(side = TOP)
        self.button_exit =  Button(self.bottomframe, text = "Exit Game", fg= "black",command = self.on_close)
        self.button_exit.pack(side = TOP )

        self.name_box()

    def printpesan(self):
        print("Masuk")

    def on_close(self):
        self.root.destroy()
        
        exit(0)

    def name_box(self):
        frame = self.topframe
        Label(frame, text='Enter username:', font=("Serif", 10)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=20, height=2, font=("Serif", 10))
        self.enter_text_widget.pack(side = BOTTOM, pady=15)
        #self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

if __name__ == '__main__':
    root = Tk()
    root.title("Othello Menu")
    root.geometry("320x220")
    Gui = Menu(root)

    root.protocol("WM_DELETE_WINDOW", Gui.on_close)
    root.mainloop()