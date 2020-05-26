import socket
import select
import sys
import msvcrt
from threading import Thread
from tkinter import *




class Gui_Chat :

    def __init__(self, master):
      self.root = master    
      self.button_inputname = None
      self.button_exit = None
      self.Clicked = True
      self.generate_gui()
      self.generate_socket()
      self.listen_thread()


    def generate_socket(self):
      self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      ip_address = '127.0.0.1'
      port = 8081
      self.server.connect((ip_address, port))


    def receive(self):
      msg = 1
      print("do space every want chat\n[quit]for exit")

      while True:
        try:
          sockets_list = [self.server]
          read_socket, write_socket, error_socket, = select.select(sockets_list, [], [],1)
          
          # if msvcrt.kbhit():
          #   read_socket.append(sys.stdin)
          if msvcrt.kbhit():
              read_socket.append(sys.stdin)
              # key = msvcrt.getche()
              # if str(key) == "b'q'": # Enter key
              #   break
                          
          for socks in read_socket:
            if socks == self.server:
                message = socks.recv(2048).decode()
                self.msg_list.insert(END, message)
            else:
                sys.stdout.write('<You>')
                message = input()
                
                if message == "[quit]": # Enter key
                  msg = 0
                  self.msg_list.insert(END, "please exit the chatbox using button exit")
                  #self.on_close()
                else:
                  self.msg_list.insert(END, "<You> " + message)
                  self.server.send(message.encode())
                  
                sys.stdout.flush()
          
          if msg == 0:
            self.server.send(message.encode())
            break
        
        except OSError:  # Possibly client has left the chat.
          break

      self.server.close()
      
    def listen_thread(self):
      receive_thread = Thread(target=self.receive)
      receive_thread.start()
      
    def send_message(self, event = None):
      msg = self.messages.get()
      self.messages.set("")  # Clears input field.
      self.server.send(msg.encode())
      self.msg_list.insert(END, "<You> " + msg)
      # if msg == "{quit}":
      #   print("selesai")
      #   self.server.send(msg.encode())    
      #   self.server.close()
      #   root.quit()


    def generate_gui(self):
      namalabel = Label(self.root, text = "Othello Chat")
      namalabel.pack()

      self.topframe = Frame(self.root)
      self.topframe.pack()
      self.bottomframe = Frame(self.root)
      self.bottomframe.pack(side = BOTTOM)

      #self.button_inputname = Button(self.bottomframe, width=10, text = "Start ", fg= "black",command = self.printpesan)
      #self.button_inputname.pack(side = BOTTOM)
      #self.button_inputname.place(x=20, y=19)
      self.button_exit =  Button(self.bottomframe, width=10, text = "Exit", fg= "black",command = self.on_close)
      #self.button_exit.pack(side = BOTTOM )
      self.button_exit.place(x=240, y=19)

      self.input_box()
      self.chat_box()


    def printpesan(self):
      print("Masuk")


    def on_close(self):
      self.root.destroy()
      temp = '[quit]'
      self.server.send(temp.encode())
      self.server.close()
      exit(0)


    def clear_box(self,event = None): 
      if self.Clicked: 
          self.Clicked = False
          self.entry_field.delete(0, "end") 
          
    def chat_box(self):
      frame = self.topframe
      scrollbar = Scrollbar(frame)
      Label(frame, text='Chat:', font=("Serif", 12)).pack(side='top', anchor='w')
      self.msg_list = Listbox(frame, height=20, width=50, yscrollcommand=scrollbar.set)
      scrollbar.pack(side=RIGHT, fill=Y)
      self.msg_list.pack(side=LEFT, fill=BOTH)
      self.msg_list.pack()
      #GUI.chat_log.config(state=tkinter.DISABLED)
      #frame.pack()


    def input_box(self):
      # frame = self.bottomframe
      # Label(frame, text='Enter message:', font=("Serif", 12)).pack(side='top', anchor='w')
      # self.enter_text_widget = Text(frame, width=60, height=1, font=("Serif", 12))
      # self.enter_text_widget.pack(side = LEFT, pady=15)
      # #self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
      # frame.pack(side='top')
      frame = self.bottomframe
      self.messages = StringVar()  
      self.entry_field = Entry(frame, textvariable=self.messages, width = 280)
      self.entry_field.bind('<FocusIn>', self.clear_box)
      self.entry_field.bind("<Return>", self.send_message)
      self.entry_field.pack()
      self.send_button = Button(frame, width=10, text="Send", command=self.send_message)
      self.send_button.pack(side=LEFT)
      #self.send_button.place(x=20, y=19)
        
    
if __name__ == '__main__':
  root = Tk()
  root.title("Chat Menu")
  root.geometry("320x420")
  Gui = Gui_Chat(root)
  root.protocol("WM_DELETE_WINDOW", Gui.on_close)
  root.mainloop()


    
