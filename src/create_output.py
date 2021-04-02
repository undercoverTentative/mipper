import json
import xml.etree.ElementTree as ET
import sqlite3
import os
import datetime

class PrintOutput:

    '''
    NAME
        PrintOutput

    DESCRIPTION
        Class for creating a mysql database, json file and
        xml file. The class needs the following arguments for
        proper operation

        host -> a IPv4 address without the port
        scantype -> a string that describes the ScanType
        FileName -> Default file output name is set to "Default" this can be change if needed

    CLASS METHODS

        AppendToJson
        AppendToXml
        AppendToDb
        Initdb
        Checkdb
        resultConvert
        writeJsonOutput
        writeXmlOutput
        dateTimeoutput
    '''


    def __init__(self, host, scantype, FileName="Default"):

        self.host = host
        if FileName == "":
            self.filename = "Default"
        else:
            self.filename = FileName
        self.scantype = scantype
        self.data = {self.scantype: []}
        self.table = "scan"
        self.xml = ET.Element(self.scantype)
        self.Checkdb()
        self.db = sqlite3.connect(self.filename + ".db")
        self.cur = self.db.cursor()
        self.Initdb()

    def AppendToJson(self,result,port):
        """
        NAME
            AppendToJson

        DESCRIPTION
            Adds a result from a port scan to the json file

        INPUT
            result  = A boolean value
            port    = A port between 0 - 65535

        RESULT
            Returns no output
        """

        res = self.resultConvert(result)

        self.data[self.scantype].append({
            "Host": self.host,
            "Port": port,
            "Result": res,
        })

    def AppendToXml(self,result,port):
        """
        NAME
            AppendToXml

        DESCRIPTION
            Adds a result from a port scan to the xml file

        INPUT
            result  = Open or Closed
            port    = A port between 0 - 65535

        RESULT
            Returns no output
        """
        res = self.resultConvert(result)

        single = ET.SubElement(self.xml, "Output")
        ET.SubElement(single, "Scan", Host=self.host, Port=str(port)).text = str(res)

    def AppendToDb(self,result,port):
        """
        NAME
            AppendToDb

        DESCRIPTION
            Adds a result from a port scan to the db file

        INPUT
            result  = Open or Closed
            port    = A port between 0 - 65535

        RESULT
            Returns no output
        """
        res = self.resultConvert(result)

        self.cur.execute("INSERT INTO scan VALUES (?,?,?,?)", (self.host,port,res,self.scantype))
        self.db.commit()

    def Initdb(self):
        """
        NAME
            Initdb

        DESCRIPTION
            Makes the default tabel if a object is made from this class

        INPUT
            Needs no input

        RESULT
            Returns no output
        """

        self.cur.execute('''CREATE TABLE scan (host text, port int, result text, scantype text)''')

    def Checkdb(self):
        """
        NAME
            Checkdb

        DESCRIPTION
            Checks if a default database with the name "Defualt.db" allready exists.
            If a database is present with the name "Default.db" then the date of
            today is appended to the Default string

        INPUT
            Needs no input

        RESULT
            Returns no output
        """

        dir = "./"
        files = os.listdir(dir)
        for file in files:
            if file.endswith("db"):
                if file == (self.filename + ".db"):
                    date = self.dateTimeoutput()
                    self.filename = "Default" + date

    def writeJsonOutput(self):
        """
        NAME
            writeJsonOutput

        DESCRIPTION
            Writes data to the .json file if all the data has been appended

        INPUT
            Needs no input

        RESULT
            Returns no output
        """

        file = self.filename + ".json"
        with open (file, 'w') as outputfile:
            json.dump(self.data,outputfile)

    def writeXmlOutput(self):
        """
        NAME
            writeXmlOutput

        DESCRIPTION
            Writes data to the .xml file if all the data has been appended

        INPUT
            Needs no input

        RESULT
            Returns no output
        """

        file = self.filename + ".xml"
        tree = ET.ElementTree(self.xml)
        tree.write(file)

    def dateTimeoutput(self):
        """
        NAME
            dateTimeoutput

        DESCRIPTION
            Get the current date and time of this machine

        INPUT
            Needs no input

        RESULT
            Returns a string with the date in the following format
            _mm_dd_YY_HH_MM_SS
        """
        today = datetime.datetime.now()
        date_time = today.strftime("_%m_%d_%Y_%H_%M_%S")
        return date_time

    def resultConvert(self,result):
        """
        NAME
            resultConvert

        DESCRIPTION
            Change the type of variable result from int to a string. if result
            is 0 this function will return a String "Open", and "Closed" for 1.

        INPUT
            Result of the type int

        RESULT
            Returns a boolean value.
        """
        if result == 0:
            return "Open"
        if result == 1:
            return "Closed"
