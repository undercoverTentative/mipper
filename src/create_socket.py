import socket
import struct
from scapy.all import *
from src.json_output import Output



class create_Socket:
    """class of creating a socket to preform a scan of the volatile ports"""
    def __init__(self, host, stport, endport, jsonOutGen=0, XmlOutGen=0, FileName="default"):
        self.host = host
        self.stport = stport
        self.endport = endport + 1
        if jsonOutGen == 0:
            self.jsonOutGen = 0
        else:
            self.jsonOutGen = jsonOutGen
        if XmlOutGen == 0:
            self.XmlOutGen = 0
        else:
            self.XmlOutGen = XmlOutGen
        if FileName == "default":
            self.FileName = "default"
        else:
            self.FileName = FileName


    def TCPportscan(self):
        p = Output(host=self.host,scantype="TCP",jsonOut=self.jsonOutGen,xmlOut=self.XmlOutGen,FileName=self.FileName)
        for dp in range(self.stport,self.endport):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(5)
            try:
                s.connect((self.host,dp))
                p.printout(0,dp)
                s.close()
            except socket.timeout:
                p.printout(1,dp)
            except ConnectionRefusedError:
                pass
                p.printout(1,dp)
            except:
                pass
                p.printout(1,dp)
        if self.jsonOutGen == 1:
            p.writeJsonOutput()

    def TCPsascan(self):
        p = Output(host=self.host,scantype="TCP SYN ACK",jsonOut=self.jsonOutGen,xmlOut=self.XmlOutGen,FileName=self.FileName)
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="S"),timeout=5,verbose=0)
            for s,r in ans:
                result = r[TCP].flags.flagrepr()
                if result == "SA":
                    p.printout(0,dp)
                else:
                    p.printout(1,dp)
        if self.jsonOutGen == 1:
            p.writeJsonOutput()

    def UDPscan(self):
        p = Output(host=self.host,scantype="UDP",jsonOut=self.jsonOutGen,xmlOut=self.XmlOutGen,FileName=self.FileName)
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/UDP(dport=dp),timeout=5,verbose=0)
            if ans:
                for s,r in ans:
                    p.printout(0,dp)
            else:
                p.printout(1,dp)
        if self.jsonOutGen == 1:
            p.writeJsonOutput()

    def XMASscan(self):
        p = Output(host=self.host,scantype="XMAS",jsonOut=self.jsonOutGen,xmlOut=self.XmlOutGen,FileName=self.FileName)
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="FPU"),timeout=5,verbose=0)
            if ans:
                for s,r in ans:
                    if r[TCP].flags.flagrepr() == "RA":
                        p.printout(1,dp)
                    else:
                        p.printout(0,dp)
            else:
                p.printout(1,dp)
        if self.jsonOutGen == 1:
            p.writeJsonOutput()
