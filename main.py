from src.create_socket import create_Socket
from src.print_output import Output
from src.create_output import PrintOutput
from src.read_db import ReadDB
from flask import Flask,render_template,request
from threading import Thread,Lock
import queue
import sys

lock = Lock()

def main(host,Sport,Eport,scantype,threads=0,jsonout=0,xmlout=0):
    Files = PrintOutput(host,scantype)
    q = queue.Queue()
    if threads > 0:
        threadlist = []
        if ((Eport - Sport) < threads):
            print("The amount of threads are more than the amount of ports to scan")
        else:
            lsOfPorts = SplitThreads(Sport,Eport,threads)
            for i in lsOfPorts:
                t = Thread(None,ThreadScan,i[0],(host,i[0],i[1],scantype,q))
                t.start()
                threadlist.append(t)
            for i in threadlist:
                i.join()
    else:
        ThreadScan(host,Sport,Eport,scantype,q)

    for i in range(q.qsize()):
        data = q.get()
        if jsonout == 1:
            Files.AppendToJson(data[1],data[2])
        if xmlout == 1:
            Files.AppendToXml(data[1],data[2])
        Files.AppendToDb(data[1],data[2])
    if jsonout == 1:
        Files.writeJsonOutput()
    if xmlout == 1:
        Files.writeXmlOutput()

def readout(dbname):
    result = ReadDB(FileName=dbname)

    if result.DBexist == False:
        print("Database doesnt exist! please check in the root folder if the given name of the database is present")
    if result.DBexist == True:
        data = result.GetDataFromDb(data_get="host,port,result,scantype")
        output = Output(host=data[1][0])
        for d in data:
            output.printout(d[2],d[1])


def ThreadScan(dsthost,Sport,Eport,scantyp,que):
    sock = create_Socket(dsthost,scantyp)
    output = Output(host=dsthost)
    for dp in range(Sport,Eport + 1):
        if scantyp == "TCPportscan":
            result = sock.TCPportscan(dp)
        if scantyp == "TCPsascan":
            result = sock.TCPsascan(dp)
        if scantyp == "UDPscan":
            result = sock.UDPscan(dp)
        if scantyp == "XMASscan":
            result = sock.XMASscan(dp)
        lock.acquire()
        output.printout(result["result"],result["port"])
        lock.release()
        data = [result["scantype"],result["result"],result["port"]]
        que.put(data)

def SplitThreads(Sport,Eport,Threads):
    list = []
    amount = (Eport - Sport)
    if (Eport - Sport) % Threads == 0:
        jumps = amount / Threads
        for i in range(Threads):
            data = [int(Sport), int(Sport + jumps)]
            list.append(data)
            Sport = Sport + int(jumps)
    else:
        jumps = int(amount / Threads)
        for i in range (Threads):
            data = [int(Sport), int(Sport + jumps)]
            list.append(data)
            Sport = Sport + int(jumps)
        leftover = amount % Threads
        leftoverdata = [int(Sport), int(Sport + leftover)]
        list.append(leftoverdata)
    return list

def hello():
    return "Hello world!"


#if __name__ == '__main__':
    #main("192.168.1.1",0,100,scantype="TCPportscan",threads=20,jsonout=0,xmlout=0)
    #readout("Default")
app = Flask(__name__)

@app.route('/<name>')
def hello(name=None):
    return render_template('test.html')

@app.route('/test', methods=['POST'])
def get_value():
    error = None
    if request.method == 'POST':
        main(request.form['Host'],int(request.form['sport']),int(request.form['eport']),request.form['scan'],int(request.form['threads']))
    else:
        error = "Invalid"
    return render_template('test.html', error=error)
