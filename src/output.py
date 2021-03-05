import json
import xml.etree.ElementTree as ET
import sqlite3
import os

class Output:
    def __init__(self, host, scantype, jsonOut, xmlOut,FileName):
        self.FileName = FileName
        self.host = host
        self.scantype = scantype
        self.data = {}
        self.jsonout = jsonOut
        self.xmlout = xmlOut
        self.xml = ET.Element(self.scantype)
        self.Checkdb()
        self.db = sqlite3.connect(self.FileName + ".db")
        self.cur = self.db.cursor()
        self.Initjson()
        self.Initdb()


    def printout(self,succes,port):
        """ Default output for printing the results """
        if succes == 0:
            result = True
            if self.jsonout == 1:
                self.AppendToJson(result,port)
            if self.xmlout == 1:
                self.AppendToXml(result,port)
            print("Host: %s         Port: %d        Result: %s" % (self.host, port, result))
            self.AppendToDb(result,port)

        if succes == 1:
            result = False
            if self.jsonout == 1:
                self.AppendToJson(result,port)
            if self.xmlout == 1:
                self.AppendToXml(result,port)
            print("Host: %s         Port: %d        Result: %s" % (self.host, port, result))
            self.AppendToDb(result,port)

    def AppendToJson(self,result,port):
        self.data[self.scantype].append({
            "Host": self.host,
            "Port": port,
            "Result": result,
        })

    def AppendToXml(self,result,port):
        single = ET.SubElement(self.xml, "Output")
        ET.SubElement(single, "Scan", Host=self.host, Port=str(port)).text = str(result)

    def AppendToDb(self,result,port):
        self.cur.execute("INSERT INTO scan VALUES ('%s','%d','%s')" % (self.host,port,result))
        self.db.commit()


    def Initjson(self):
        self.data[self.scantype] = []

    def Initdb(self):
        self.cur.execute('''CREATE TABLE scan (host text, port int, result bool)''')


    def Checkdb(self):
        dir = "./"
        files = os.listdir(dir)
        for file in files:
            if file.endswith("db"):
                path = os.path.join(dir, file)
                os.remove(path)
                
    def writeJsonOutput(self):
        file = self.FileName + ".json"
        with open (file, 'w') as outputfile:
            json.dump(self.data,outputfile)

    def writeXmlOutput(self):
        file = self.FileName + ".xml"
        tree = ET.ElementTree(self.xml)
        tree.write(file)
