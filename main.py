from src.create_socket import create_Socket
from src.output import Output
from threading import Thread
import queue
import sys

def main(host,Sport,Eport,scantype,threads=0):
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
        print(q.get())



def ThreadScan(dsthost,Sport,Eport,scantyp,que):
    sock = create_Socket(dsthost,scantyp)
    output = Output(host=dsthost,scantype=scantyp)
    for dp in range(Sport,Eport):
        result = sock.TCPportscan(dp)
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
    main("192.168.1.1",0,100,scantype="TCPportscan",threads=0)
