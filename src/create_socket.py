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
            try:
                s.connect((self.host,dp))
                print("Host: %s         Port: %d        Result: %s" % (self.host, dp, "Succes"))
                s.close()
            except socket.timeout:
                print("Timeout error has occured")
            except ConnectionRefusedError:
                pass
            except:
                pass

    def TCPsascan(self):
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="S"),timeout=5,verbose=0)
            for s,r in ans:
                result = r[TCP].flags.flagrepr()
                if result == "SA":
                    print("Host: %s         Port: %d        Result: %s" % (self.host, dp, "Succes"))
                else:
                    print("Host: %s         Port: %d        Result: %s" % (self.host, dp, "Fail"))
