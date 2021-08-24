import socket	
import time

def main():
    try:
        s = socket.socket()		 

        port = 3000		

        s.bind(('192.168.1.38', port))		 
        print("socket binded to %s" %(port))

        s.listen(3)	 
        print("socket is listening")
        c, addr = s.accept()

        while True:
            c.send(str([1,2]).encode())
            time.sleep(0.2)

    except ConnectionAbortedError:
        s.close()
        pass

    except KeyboardInterrupt:
        s.close()
        exit()


if __name__ == "__main__":
    while True:
        main()