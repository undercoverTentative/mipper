from src.create_tcp_socket import create_Socket
import sys

def main():


    sock = create_Socket("127.0.0.1")
    sock.UDPportscan()


if __name__ == '__main__':
    main()
