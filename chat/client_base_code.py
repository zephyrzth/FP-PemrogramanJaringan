import socket
import select
import sys
import msvcrt
from threading import Thread
from tkinter import *

def receive():
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  ip_address = '127.0.0.1'
  port = 8081
  server.connect((ip_address, port))
  msg = 1
  print("do space every want chat\n[quit]for exit")

  while True:
    try:
        sockets_list = [server]
        read_socket, write_socket, error_socket, = select.select(sockets_list, [], [],1)
        
        # if msvcrt.kbhit():
        #   read_socket.append(sys.stdin)
        if msvcrt.kbhit():
            read_socket.append(sys.stdin)
            # key = msvcrt.getche()
            # if str(key) == "b'q'": # Enter key
            #   break
                        
        for socks in read_socket:
          if socks == server:
              message = socks.recv(2048).decode()
              print(message)
          else:
              sys.stdout.write('<You>')
              message = input()
              if message == "[quit]": # Enter key
                msg = 0
              
              server.send(message.encode())
              sys.stdout.flush()
        
        if msg == 0:
          server.send(message.encode())
          break
       
    except OSError:  # Possibly client has left the chat.
      break

  server.close()

receive_thread = Thread(target=receive)
receive_thread.start()
receive_thread.join()