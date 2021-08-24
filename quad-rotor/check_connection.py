import socket 

addr = "192.168.1.1"

s = socket.socket()          
  
port = 3000               
  
# connect to the server on local computer 
s.connect((addr, port)) 
  
# receive data from the server

while True: 
    
    # print(s.recv(1024)) 
    data = s.recv(1024)
    data = tuple(data)
    print(data)

s.close()