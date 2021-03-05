import json

class Output:
    def __init__(self, host, scantype, jsonOut=0, xmlOut=0,FileName="default"):
        self.host = host
        self.scantype = scantype
        self.data = {}
        self.json = jsonOut
        self.json = xmlOut
        self.FileName = FileName
        self.Initjson()
        self.InitXml()


    def printout(self,succes,port):
        """ Default output for printing the results """
        if succes == 0:
            result = True
            if self.json == 1:
                self.AppendToJson(result,port)
            print("Host: %s         Port: %d        Result: %s" % (self.host, port, result))

        if succes == 1:
            result = False
            if self.json == 1:
                self.AppendToJson(result,port)
            print("Host: %s         Port: %d        Result: %s" % (self.host, port, result))

    def AppendToJson(self,result,port):
        self.data[self.scantype].append({
            "Host": self.host,
            "Port": port,
            "Result": result,
        })


    def Initjson(self):
        self.data[self.scantype] = []

    def InitXml(self):
        print("Test")

    def writeJsonOutput(self):
        file = self.FileName + ".json"
        with open (file, 'w') as outputfile:
            json.dump(self.data,outputfile)
