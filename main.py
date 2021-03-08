from src.create_socket import create_Socket
from src.output import Output
import sys

def main():


    sock = create_Socket("192.168.1.1",scantype="UDP")
    output = Output(host=sock.host,scantype=sock.scantype, xmlOut=1)
    for dp in range(50,55):
        result = sock.XMASscan(dp)
        output.printout(result["result"],result["port"])
    if output.xmlout == 1:
        output.writeXmlOutput()

if __name__ == '__main__':
    main()
