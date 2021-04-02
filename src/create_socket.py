import socket
import struct
from scapy.all import *
from src.print_output import Output



class create_Socket:
    '''
    NAME
        create_Socket

    DESCRIPTION
        Class for creating a object that is capable of
        executing different kind op port scan. This class has the
        capability to preform the following port scans.

        -   TCPportscan (Connect)
        -   TCPsascan (SYN/ACK)
        -   UDPscan
        -   XMASscan (TCP XMAS scan)

        The following parameters have to be deliverd upon creating
        an object

        -   host -> A IPv4 address wich will be tested
        -   scantype -> A string that represent the executed scan type

    CLASS METHODS

        TCPportscan
        TCPsascan
        UDPscan
        XMASscan
    '''

    def __init__(self, host, scantype):
        self.host = host
        self.scantype = scantype
        self.output =  {"scantype": self.scantype,
                        "result": "",
                        "port": ""}

    def TCPportscan(self,dp):

        """
        NAME
            TCPportscan

        DESCRIPTION
            Executes a TCP connect scan for a single port

        INPUT
            dp = A type int between 1-65535. This represents the port for the host to test

        RESULT
            Returns a list
                ['scantype','result','port']
            result 0 means the connection has been made
            result 1 means the connection could not be made.
        """
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
        """
        NAME
            TCPsascan

        DESCRIPTION
            Executes a TCP SYN/ACK scan with the scapy module for a single port

        INPUT
            dp = A type int between 1-65535. This represents the port for the host to test

        RESULT
            Returns a list
                ['scantype','result','port']
            result 0 means the SYN/ACK handshake could be preformed
            result 1 means the SYN/ACK handshake could not be preformed
        """
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
        """
        NAME
            UDPscan

        DESCRIPTION
            Executes a UDP scan with the scapy module for a single port

        INPUT
            dp = A type int between 1-65535. This represents the port for the host to test

        RESULT
            Returns a list
                ['scantype','result','port']
            result 0 means a anwser have been received
            result 1 means no awnser could be receive due to timeout
        """
        self.output["port"] = dp
        ans, unans = sr(IP(dst=self.host)/UDP(dport=dp),timeout=5,verbose=0)
        if ans:
            for s,r in ans:
                self.output["result"] = 0
                return self.output
        else:
            self.output["result"] = 1
            return self.output

    def XMASscan(self,dp):
        """
        NAME
            XMASscan

        DESCRIPTION
            Executes a XMAS scan with the scapy module for a single port

        INPUT
            dp = A type int between 1-65535. This represents the port for the host to test

        RESULT
            Returns a list
                ['scantype','result','port']
            result 0 means a anwser have been received
            result 1 means no awnser could be receive due to timeout
        """
        self.output["port"] = dp
        ans, unans = sr(IP(dst=self.host)/TCP(dport=dp,flags="FPU"),timeout=5,verbose=0)
        if ans:
            for s,r in ans:
                if r[TCP].flags.flagrepr() == "RA":
                    self.output["result"] = 0
                    return self.output
                else:
                    self.output["result"] = 1
                    return self.output
        else:
            self.output["result"] = 1
            return self.output
