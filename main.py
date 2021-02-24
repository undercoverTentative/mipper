from src.create_socket import create_Socket
import sys

def main():


<<<<<<< HEAD
    sock = create_Socket("127.0.0.1",39,41)
    sock.TCPportscan()
=======
    sock = create_Socket("127.0.0.1",1,100)
    sock.TCPsascan()
>>>>>>> TCP_SYN_ACK

if __name__ == '__main__':
    main()
