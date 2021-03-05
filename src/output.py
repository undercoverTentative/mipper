import json
import xml.etree.ElementTree as ET

class Output:
    def __init__(self, host, scantype, jsonOut, xmlOut,FileName="default"):
        self.host = host
        self.scantype = scantype
        self.data = {}
        self.jsonout = jsonOut
        self.xmlout = xmlOut
        self.xml = ET.Element(self.scantype)
        self.FileName = FileName
        self.Initjson()


    def printout(self,succes,port):
        """ Default output for printing the results """
        if succes == 0:
            result = True
            if self.jsonout == 1:
                self.AppendToJson(result,port)
            if self.xmlout == 1:
                self.AppendToXml(result,port)
            print("Host: %s         Port: %d        Result: %s" % (self.host, port, result))

        if succes == 1:
            result = False
            if self.jsonout == 1:
                self.AppendToJson(result,port)
            if self.xmlout == 1:
                self.AppendToXml(result,port)
            print("Host: %s         Port: %d        Result: %s" % (self.host, port, result))

    def AppendToJson(self,result,port):
        self.data[self.scantype].append({
            "Host": self.host,
            "Port": port,
            "Result": result,
        })

    def AppendToXml(self,result,port):
        single = ET.SubElement(self.xml, "Output")
        ET.SubElement(single, "Scan", Host=self.host, Port=str(port)).text = str(result)


    def Initjson(self):
        self.data[self.scantype] = []
        print("Test1")

    def writeJsonOutput(self):
        file = self.FileName + ".json"
        with open (file, 'w') as outputfile:
            json.dump(self.data,outputfile)

    def writeXmlOutput(self):
        file = self.FileName + ".xml"
        tree = ET.ElementTree(self.xml)
        tree.write(file)
