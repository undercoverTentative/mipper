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
                self.Output(0,self.host,dp)
                s.close()
            except socket.timeout:
                self.Output(1,self.host,dp)
            except ConnectionRefusedError:
                pass
                self.Output(1,self.host,dp)
            except:
                pass
                self.Output(1,self.host,dp)

    def TCPsascan(self):
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="S"),timeout=5,verbose=0)
            for s,r in ans:
                result = r[TCP].flags.flagrepr()
                if result == "SA":
                    self.Output(0,self.host,dp)
                else:
                    self.Output(1,self.host,dp)

    def UDPscan(self):
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/UDP(dport=dp),timeout=5,verbose=0)
            if ans:
                for s,r in ans:
                    self.Output(0,self.host,dp)
            else:
                self.Output(1,self.host,dp)

    def XMASscan(self):
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="FPU"),timeout=5,verbose=0)
            if ans:
                for s,r in ans:
                    if r[TCP].flags.flagrepr() == "RA":
                        self.Output(1,self.host,dp)
                    else:
                        self.Output(0,self.host,dp)
            else:
                self.Output(1,self.host,dp)

    def Output(self,succes, host, port):
        """Default output for printing the results"""
        if succes == 0:
            print("Host: %s         Port: %d        Result: %s" % (host, port, "Succes"))
        if succes == 1:
            print("Host: %s         Port: %d        Result: %s" % (host, port, "Fail"))
