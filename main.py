from src.create_socket import create_Socket
import sys

def main():


    sock = create_Socket("8.8.8.8",50,56)
    sock.TCPportscan()

if __name__ == '__main__':
    main()
