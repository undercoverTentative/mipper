from src.create_socket import create_Socket
import sys

def main():


    sock = create_Socket("192.168.1.1",50,56,scantype="TCP",jsonOutGen=1,XmlOutGen=1)
    sock.Start()

if __name__ == '__main__':
    main()
