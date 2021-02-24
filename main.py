from src.create_socket import create_Socket
import sys

def main():


    sock = create_Socket("127.0.0.1",39,41)
    sock.TCPportscan()

if __name__ == '__main__':
    main()
