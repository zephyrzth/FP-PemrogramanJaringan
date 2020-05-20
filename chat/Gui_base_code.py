from tkinter import *

class Gui_Chat :

    def __init__(self, master):
        self.root = master    
        self.button_inputname = None
        self.button_exit = None
        self.generate_gui()   

    def generate_gui(self):
        namalabel = Label(self.root, text = "Othello Chat")
        namalabel.pack()
        self.topframe = Frame(self.root)
        self.topframe.pack()
        self.bottomframe = Frame(self.root)
        self.bottomframe.pack(side = BOTTOM)
        
        self.button_inputname = Button(self.bottomframe, text = "Start ", fg= "black",command = self.printpesan)
        self.button_inputname.pack(side = RIGHT)
        self.button_exit =  Button(self.bottomframe, text = "Exit", fg= "black",command = self.on_close)
        self.button_exit.pack(side = LEFT )

        self.input_box()
        self.chat_box()

    def printpesan(self):
        print("Masuk")

    def on_close(self):
        self.root.destroy()
        
        exit(0)

    def chat_box(self):
        frame = self.topframe
        Label(frame, text='Chat:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12))
        #scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        #self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        #scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def input_box(self):
        frame = self.bottomframe
        Label(frame, text='Enter message:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side = BOTTOM, pady=15)
        #self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')
        

if __name__ == '__main__':
    root = Tk()
    root.title("Chat Menu")
    root.geometry("320x420")
    Gui = Gui_Chat(root)

    root.protocol("WM_DELETE_WINDOW", Gui.on_close)
    root.mainloop()

    