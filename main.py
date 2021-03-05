from src.create_socket import create_Socket
import sys

def main():


    sock = create_Socket("192.168.1.1",50,56,scantype="XMAS",jsonOutGen=0,XmlOutGen=0)
    sock.Start()

if __name__ == '__main__':
    main()
