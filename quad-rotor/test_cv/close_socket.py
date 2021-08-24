import socket

s = socket.socket()

port = 3000

s.bind(('127.0.0.1', port))		 
print("socket binded to %s" %(port))

s.listen(5)	 
print("socket is listening")
c, addr = s.accept()

s.close()