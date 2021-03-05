from src.create_socket import create_Socket
import sys

def main():


    sock = create_Socket("192.168.1.1",50,56)
    sock.TCPportscan()

if __name__ == '__main__':
    main()
