import socket
import struct
from scapy.all import *
from src.print_output import Output



class create_Socket:
    """class of creating a socket to preform a scan of the volatile ports"""

    def __init__(self, host, scantype):
        self.host = host
        self.scantype = scantype
        self.output =  {"scantype": self.scantype,
                        "result": "",
                        "port": ""}

    def TCPportscan(self,dp):
        self.output["port"] = str(dp)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect((self.host,dp))
            self.output["result"] = 0
            return self.output
            s.close()
        except socket.timeout:
            self.output["result"] = 1
            return self.output
        except ConnectionRefusedError:
            pass
            self.output["result"] = 1
            return self.output
        except:
            pass
            self.output["result"] = 1
            return self.output


    def TCPsascan(self,dp):
        self.output["port"] = dp
        ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="S"),timeout=5,verbose=0)
        for s,r in ans:
            result = r[TCP].flags.flagrepr()
            if result == "SA":
                self.output["result"] = 0
                return self.output
            else:
                self.output["result"] = 1
                return self.output


    def UDPscan(self,dp):
        self.output["port"] = dp
        ans, unans = sr(IP(dst=self.host)/UDP(dport=dp),timeout=5,verbose=0)
        if ans:
            for s,r in ans:
                self.output["result"] = 1
                return self.output
        else:
            self.output["result"] = 0
            return self.output

    def XMASscan(self,dp):
        self.output["port"] = dp
        ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="FPU"),timeout=5,verbose=0)
        if ans:
            for s,r in ans:
                if r[TCP].flags.flagrepr() == "RA":
                    self.output["result"] = 1
                    return self.output
                else:
                    self.output["result"] = 0
                    return self.output
        else:
            self.output["result"] = 1
            return self.output
