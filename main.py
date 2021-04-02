from flask import Flask,render_template,request,send_from_directory,send_file
import sys,os,sqlite3,re
from threading import Thread,Lock
from src.create_socket import create_Socket
from src.print_output import Output
from src.create_output import PrintOutput
import queue

lock = Lock()
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)


def run_mipper(host,Sport,Eport,scantype,threads,jsonout,xmlout):
    Files = PrintOutput(host,scantype)
    global last_scan
    last_scan = [Files.filename + ".db", Files.filename + ".xml", Files.filename + ".json"]
    q = queue.Queue()
    if threads > 1:
        threadlist = []
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

def get_old_scan_result():
    data = []
    dir = "./"
    files = os.listdir(dir)
    for file in files:
        if file.endswith("db"):
            if file == "Default":
                data.append(file)
            else:
                data.append(file[8:-3])
    return data

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
    older_scans_result = []
    if request.method == 'POST':
        if int(request.form['sport']) > 0 and int(request.form['sport']) <= 65535:
            if int(request.form['eport']) > 0 and int(request.form['eport']) <= 65535:
                if int(request.form['sport']) < int(request.form['eport']):
                    if ((int(request.form['eport']) - int(request.form['sport'])) < int(request.form['threads'])):
                        error = "The amount of threads are more than the amount of ports to scan"
                        return render_template('error.html', error=error)
                    else:
                        run_mipper(request.form['Host'],int(request.form['sport']),int(request.form['eport']),request.form['scan'],int(request.form['threads']),int(request.form['jsonout']),int(request.form['xmlout']))
                        older_scans_result = get_old_scan_result()
                        con = sqlite3.connect(last_scan[0])
                        cursor = con.cursor()
                        cursor.execute("SELECT * FROM scan ORDER BY port ASC")
                        data = cursor.fetchall()
                        return render_template('result.html', data=data, xml_present=os.path.isfile(last_scan[1]), json_present=os.path.isfile(last_scan[2]), older_scans_result=older_scans_result)
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
    print(last_scan[0])
    path = os.path.join(app.root_path, last_scan[0])
    return send_file(path)

@app.route('/download_json', methods=['GET','POST'])
def download_json():
    print(last_scan[2])
    path = os.path.join(app.root_path, last_scan[2])
    return send_file(path)

@app.route('/download_xml', methods=['GET','POST'])
def download_xml():
    print(last_scan[1])
    path = os.path.join(app.root_path, last_scan[1])
    return send_file(path)

@app.route('/old_results', methods=['GET','POST'])
def show_old_results():
    older_scans_result = []
    if request.method == "POST":
        result = re.match(r"(\A\d{2}[_]\d{2}[_]\d{4}[_]\d{2}[_]\d{2}[_]\d{2}\b|^\s*$)",request.form['filename'])
        if result == None:
            error = "Input didn't match the request format to retreive infromation from old scan results.\
            Format has to be as follow '01_01_0101_01_01'"
            return render_template("error.html", error=error)
        else:
            if request.form['filename'] == "":
                dbfile = "Default.db"
                xmlfile = "Default.xml"
                jsonfile = "Default.json"
            else:
                dbfile = "Default_" + request.form['filename'] + ".db"
                xmlfile = "Default_" + request.form['filename'] + ".xml"
                jsonfile = "Default_" + request.form['filename'] + ".json"
            older_scans_result = get_old_scan_result()
            con = sqlite3.connect(dbfile)
            cursor = con.cursor()
            cursor.execute("SELECT * FROM scan ORDER BY port ASC")
            data = cursor.fetchall()
            return render_template('result.html', data=data, xml_present=os.path.isfile(xmlfile), json_present=os.path.isfile(jsonfile), older_scans_result=older_scans_result)


@app.route('/new_scan', methods=['GET','POST'])
def back_to_main_page():
    return render_template('test.html')
