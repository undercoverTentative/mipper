import json
import xml.etree.ElementTree as ET
import sqlite3
import os
import datetime

class PrintOutput:
    def __init__(self, host, scantype, jsonOut=0, xmlOut=0,FileName="Default"):
        self.host = host
        if FileName == "":
            self.filename = "Default"
        else:
            self.filename = FileName
        self.scantype = scantype
        self.data = {}
        self.table = "scan"
        self.jsonout = jsonOut
        self.xmlout = xmlOut
        self.xml = ET.Element(self.scantype)
        self.Checkdb()
        self.db = sqlite3.connect(self.filename + ".db")
        self.cur = self.db.cursor()
        self.Initjson()



    def AppendToJson(self,result,port):
        """ Appending result to the Json output """

        self.data[self.scantype].append({
            "Host": self.host,
            "Port": port,
            "Result": result,
        })

    def AppendToXml(self,host,result,port):
        """ Appending result to the XML output """

        single = ET.SubElement(self.xml, "Output")
        ET.SubElement(single, "Scan", Host=self.host, Port=str(port)).text = str(result)

    def AppendToDb(self,result,port):
        """ Appending result to the Database output """

        self.cur.execute("INSERT INTO scan VALUES ('?','?','?')", (self.host,port,result))
        self.db.commit()


    def Initjson(self):
        """ Creating default Json vars """

        self.data[self.scantype] = []

    def Initdb(self):
        """ Creating default database """

        self.cur.execute('''CREATE TABLE scan (host text, port int, result bool)''')


    def Checkdb(self):
        """ Check if DB has been created and remove default database """

        dir = "./"
        files = os.listdir(dir)
        for file in files:
            if file.endswith("db"):
                if file == (self.filename + ".db"):
                    date = self.dateTimeoutput()
                    self.filename = "Default" + date
                    print(self.filename)

    def writeJsonOutput(self):
        """ Creating default Json output file """

        file = self.FileName + ".json"
        with open (file, 'w') as outputfile:
            json.dump(self.data,outputfile)

    def writeXmlOutput(self):
        """ Creating default XML output file """

        file = self.FileName + ".xml"
        tree = ET.ElementTree(self.xml)
        tree.write(file)

    def dateTimeoutput(self):
        today = datetime.datetime.now()
        date_time = today.strftime("_%m_%d_%Y_s%H_%M_%S")
        return date_time
