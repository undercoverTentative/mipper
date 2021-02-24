from src.create_socket import create_Socket
import sys

def main():


    sock = create_Socket("127.0.0.1",1,100)
    sock.TCPsascan()

if __name__ == '__main__':
    main()
