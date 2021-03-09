from src.create_socket import create_Socket
from src.print_output import Output
from src.create_output import PrintOutput
from threading import Thread
import queue
import sys

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



def ThreadScan(dsthost,Sport,Eport,scantyp,que):
    sock = create_Socket(dsthost,scantyp)
    output = Output(host=dsthost,scantype=scantyp)
    for dp in range(Sport,Eport):
        if scantyp == "TCPportscan":
            result = sock.TCPportscan(dp)
        if scantyp == "TCPsascan":
            result = sock.TCPsascan(dp)
        if scantyp == "UDPscan":
            result = sock.UDPscan(dp)
        if scantyp == "XMASscan":
            result = sock.XMASscan(dp)
        output.printout(result["result"],result["port"])
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


if __name__ == '__main__':
    main("192.168.1.1",0,100,scantype="TCPportscan",threads=20,jsonout=1,xmlout=1)
