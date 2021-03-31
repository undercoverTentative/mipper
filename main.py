from flask import Flask,render_template,request,send_from_directory,send_file
import sys,os,sqlite3
from threading import Thread,Lock
from src.create_socket import create_Socket
from src.print_output import Output
from src.create_output import PrintOutput
from src.read_db import ReadDB
import queue

lock = Lock()
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

def run_mipper(host,Sport,Eport,scantype,threads,jsonout,xmlout):
    Files = PrintOutput(host,scantype)
    q = queue.Queue()
    if threads > 1:
        threadlist = []
        if ((Eport - Sport) < threads):
            print("The amount of threads are more than the amount of ports to scan")
        else:
            lsOfPorts = SplitThreads(Sport,Eport,threads)
            for i in lsOfPorts:
                t = Thread(None,ThreadScan,i,(host,(i[0]),i[1],scantype,q))
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
        print("here is come")
        Files.writeJsonOutput()
    if xmlout == 1:
        Files.writeXmlOutput()

def ThreadScan(dsthost,Sport,Eport,scantyp,que):
    sock = create_Socket(dsthost,scantyp)
    output = Output(host=dsthost)
    for dp in range(Sport,Eport):
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
    if Sport == 1:
        amount = Eport
    else:
        amount = (Eport - Sport)
    if (amount) % Threads == 0:
        jumps = int(amount / Threads)
        for i in range(Threads):
            data = [int(Sport), int(Sport + jumps)]
            list.append(data)
            Sport = Sport + int(jumps)
    else:
        jumps = int(amount / Threads)
        for i in range(Threads):
            data = [int(Sport), int(Sport + jumps)]
            list.append(data)
            Sport = Sport + int(jumps)
        leftover = amount % Threads
        leftoverdata = [int(Sport), int(Sport + leftover)]
        list.append(leftoverdata)
    return list

@app.route("/")
def hello():
    return render_template('test.html')

@app.route('/test', methods=['GET','POST'])
def get_value():
    error = None
    scan = None
    if request.method == 'POST':
        if int(request.form['sport']) > 0 and int(request.form['sport']) <= 65535:
            if int(request.form['eport']) > 0 and int(request.form['eport']) <= 65535:
                if int(request.form['sport']) < int(request.form['eport']):
                    run_mipper(request.form['Host'],int(request.form['sport']),int(request.form['eport']),request.form['scan'],int(request.form['threads']),int(request.form['jsonout']),int(request.form['xmlout']))
                    con = sqlite3.connect("Default.db")
                    cursor = con.cursor()
                    cursor.execute("SELECT * FROM scan ORDER BY port ASC")
                    data = cursor.fetchall()
                    return render_template('result.html', data=data)
                else:
                    error = "End port needs to be greater than start port"
                    return render_template('error.html', error=error)
            else:
                error = "End port needs to be between 0-65535"
                return render_template('error.html', error=error)
        else:
            error = "Start port needs to be between 0-65535"
            return render_template('error.html', error=error)
    else:
        error = "Wrong request received"
        return render_template('error.html', error=error)

@app.route('/download_db', methods=['GET','POST'])
def download_db():
    path = os.path.join(app.root_path, "Default.db")
    return send_file(path)

@app.route('/download_json', methods=['GET','POST'])
def download_json():
    path = os.path.join(app.root_path, "Default.json")
    return send_file(path)

@app.route('/download_xml', methods=['GET','POST'])
def download_xml():
    path = os.path.join(app.root_path, "Default.xml")
    return send_file(path)
