import json
import xml.etree.ElementTree as ET
import sqlite3
import os

class Output:

    '''
    NAME
        Output

    DESCRIPTION
        Class for creating a standard output to print into the
        CLI

        host -> a IPv4 address without the port

    CLASS METHODS

        PrintOutput
    '''

    def __init__(self, host):
        self.host = host

    def printout(self,succes,port):
        """
        NAME
            printoutput

        DESCRIPTION
            creates a default output to print for every single result

        INPUT
            succes = A type int between 0-1. This represents 0 for True and 1 for False
            port = A type int between 0-65535. This represents the port that have been tested

        RESULT
            Prints the result of a scan to the CLI with the print statement
        """

        if succes == 0:
            result = "Open"
            print("Host: %s         Port: %s        Result: %s" % (self.host, port, result))
        else:
            result = "Closed"
            print("Host: %s         Port: %s        Result: %s" % (self.host, port, result))
