import json
import xml.etree.ElementTree as ET
import sqlite3
import os

class Output:
    def __init__(self, host, scantype, jsonOut=0, xmlOut=0,FileName="Default"):
        self.FileName = FileName
        self.host = host
        self.scantype = scantype


    def printout(self,succes,port):
        """ Default output for printing the results """
        if succes == 0:
            result = True
            print("Host: %s         Port: %s        Result: %s" % (self.host, port, result))

        if succes == 1:
            result = False
            print("Host: %s         Port: %s        Result: %s" % (self.host, port, result))
    
