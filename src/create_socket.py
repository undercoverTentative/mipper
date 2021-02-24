import socket
import struct
from scapy.all import *


class create_Socket:
    """class of creating a socket to preform a scan of the volatile ports"""
    def __init__(self, host, stport, endport):
        self.host = host
        self.stport = stport
        self.endport = endport + 1

    def TCPportscan(self):
        for dp in range(self.stport,self.endport):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(5)
            try:
                s.connect((self.host,dp))
                print("Connetion have been made to port: " + str(dp))
                s.close()
            except socket.timeout:
                print("Timeout error has occured")
            except ConnectionRefusedError:
                pass
            except:
                pass

    def TCPsascan(self):
        for dp in range(self.stport,self.endport):
            ans = sr(IP(dst=self.host)/TCP(dport=dp,flags="S"),timeout=5,verbose=0)
            print(ans)


    def UDPscan(self):
        for dp in range(self.stport,self.endport):
            ans = sr(IP(dst=self.host)/UDP(dport=dp),timeout=5,verbose=0)
            print(ans)
