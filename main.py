from src.create_socket import create_Socket
import sys

def main():


    sock = create_Socket("93.184.220.29",79,80)
    sock.TCPsascan()

if __name__ == '__main__':
    main()
