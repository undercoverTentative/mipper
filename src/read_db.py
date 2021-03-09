import sqlite3
import os

class ReadDB:
    def __init__(self, FileName):
        self.DBexist = None
        if FileName == "":
            self.filename = "Default"
        else:
            self.filename = FileName
        self.db = None
        self.Checkdb()
        if self.DBexist == True:
            self.db = sqlite3.connect(self.filename + ".db")
            self.cur = self.db.cursor()


    def Checkdb(self):
        """ Check if DB exists """

        dir = "./"
        files = os.listdir(dir)
        for file in files:
            if file.endswith("db"):
                if file == (self.filename + ".db"):
                    self.DBexist = True
                else:
                    self.DBexist = False

    def GetDataFromDb(self,data_get):
        """ Retreive data from DB """
        query = "SELECT " + data_get + " FROM scan"
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data
