import socket
import struct
from scapy.all import *
from src.output import Output



class create_Socket:
    """class of creating a socket to preform a scan of the volatile ports"""

    def __init__(self, host, stport, endport, scantype, jsonOutGen=0, XmlOutGen=0, FileName=None):
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
        if FileName == None:
            self.FileName = "default"
        else:
            self.FileName = FileName
        self.scantype = scantype
        self.p = Output(host=self.host,scantype=self.scantype,jsonOut=self.jsonOutGen,xmlOut=self.XmlOutGen,FileName=self.FileName)


    def TCPportscan(self):
        for dp in range(self.stport,self.endport):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(5)
            try:
                s.connect((self.host,dp))
                self.p.printout(0,dp)
                s.close()
            except socket.timeout:
                self.p.printout(1,dp)
            except ConnectionRefusedError:
                pass
                self.p.printout(1,dp)
            except:
                pass
                self.p.printout(1,dp)
        self.OutputGen()

    def TCPsascan(self):
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="S"),timeout=5,verbose=0)
            for s,r in ans:
                result = r[TCP].flags.flagrepr()
                if result == "SA":
                    self.p.printout(0,dp)
                else:
                    self.p.printout(1,dp)
        self.OutputGen()

    def UDPscan(self):
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/UDP(dport=dp),timeout=5,verbose=0)
            if ans:
                for s,r in ans:
                    self.p.printout(0,dp)
            else:
                self.p.printout(1,dp)
        self.OutputGen()

    def XMASscan(self):
        for dp in range(self.stport,self.endport):
            ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="FPU"),timeout=5,verbose=0)
            if ans:
                for s,r in ans:
                    if r[TCP].flags.flagrepr() == "RA":
                        self.p.printout(1,dp)
                    else:
                        self.p.printout(0,dp)
            else:
                self.p.printout(1,dp)
        self.OutputGen()

    def OutputGen(self):
        if self.jsonOutGen == 1:
            self.p.writeJsonOutput()
        if self.XmlOutGen == 1:
            self.p.writeXmlOutput()

    def Start(self):
        if self.scantype == "TCP":
            self.TCPportscan()
        if self.scantype == "TCP SYN ACK":
            self.TCPsascan()
        if self.scantype == "UDP":
            self.UDPscan()
        if self.scantype == "XMAS":
            self.XMASscan()
