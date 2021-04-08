from flask import Flask,render_template,request,send_from_directory,send_file
import sys,os,sqlite3,re,queue,ipaddress
from threading import Thread,Lock
from src.create_socket import create_Socket
from src.print_output import Output
from src.create_output import PrintOutput


lock = Lock()
app = Flask(__name__)

if __name__ == '__main__':
    app.run()


def run_mipper(host,Sport,Eport,scantype,threads,jsonout,xmlout):

    """
    NAME
        run_mipper

    DESCRIPTION
        This function will execute the mipper program. The function will create
        the needed threads that have been specified by user in the flask frontend.
        It alsof will seperate the amount of specified ports into list so each
        thread will have the same amount of workload.

    INPUT
        host  = A IPv4 address wich has to be scanned
        Sport = Starting port in the range to execute the scan. Has to be a type int an a value between 1-65535
        Eport = Ending Port in the range to execute the scan. Has to be a type int an a value between 1-65535
        scantype = A string value with the folling options;  "TCPportscan", "TCPsascan", "UDPscan", "XMASscan"
        threads = The amount of threads the user want to use. Has to be a type int
        jsonout = If value is set to 1 a .json file will be created to display the old_results
        xmlout = If value is set to 1 a .xml file will be created to display the old_results

    RESULT
        Returns no output
    """

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
        Eport = Eport + 1
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
    """
    NAME
        ThreadScan

    DESCRIPTION
        This function will execute the mipper program. The function will create
        the needed threads that have been specified by user in the flask frontend.
        It alsof will seperate the amount of specified ports into list so each
        thread will have the same amount of workload.

    INPUT
        dsthost  = A IPv4 address of the host that have to be scanned
        Sport = Starting port in the range to execute the scan. Has to be a type int an a value between 1-65535
        Eport = Ending Port in the range to execute the scan. Has to be a type int an a value between 1-65535
        scantype = A string value with the folling options;  "TCPportscan", "TCPsascan", "UDPscan", "XMASscan"
        que = A que for storing the data of the results for different Threads

    RESULT
        Returns no output
    """
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

    """
    NAME
        get_old_scan_result

    DESCRIPTION
        This function will output the filename of old scan result for displaying
        in the html frontend.

    INPUT
        Needs no input

    RESULT
        Returns a list of filenames from old scan results
    """
    data = []
    dir = "./"
    files = os.listdir(dir)
    for file in files:
        if file.endswith("db"):
            if file == "Default.db":
                data.append(file[:-3])
            else:
                data.append(file[8:-3])
    return data

def SplitThreads(Sport,Eport,Threads):

    """
    NAME
        SplitThreads

    DESCRIPTION
        This function will split the amount of ports (Sport - Eport) into a list of ranges for
        the threads to execute the port scans.

    INPUT
        Sport = Starting port in the range to execute the scan. Has to be a type int an a value between 1-65535
        Eport = Ending Port in the range to execute the scan. Has to be a type int an a value between 1-65535
        threads = The amount of threads to devide the ranges

    RESULT
        Returns a list ranges with each item in the list consist of a Sport and Eport.
    """

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
                    if ((int(request.form['eport']) - int(request.form['sport'])) >= int(request.form['threads'])):
                        try:
                            ipaddress.ip_address(request.form['Host'])
                            run_mipper(request.form['Host'],int(request.form['sport']),int(request.form['eport']),request.form['scan'],int(request.form['threads']),int(request.form['jsonout']),int(request.form['xmlout']))
                            older_scans_result = get_old_scan_result()
                            con = sqlite3.connect(last_scan[0])
                            cursor = con.cursor()
                            cursor.execute("SELECT * FROM scan ORDER BY port ASC")
                            data = cursor.fetchall()
                            return render_template('result.html', data=data, xml_present=os.path.isfile(last_scan[1]), json_present=os.path.isfile(last_scan[2]), older_scans_result=older_scans_result)
                        except ValueError:
                            error = "The given IPaddress by the user doesnt represent a IPv4 address"
                            return render_template('error.html', error=error)
                    else:
                        error = "The amount of threads are more than the amount of ports to scan"
                        return render_template('error.html', error=error)

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
        result = re.match(r"(\A\d{2}[_]\d{2}[_]\d{4}[_]\d{2}[_]\d{2}[_]\d{2}\b|\ADefault)",request.form['filename'])
        if result == None:
            error = "Input didn't match the request format to retreive infromation from old scan results.\
            Format has to be as follow '01_01_0101_01_01' or Default"
            return render_template("error.html", error=error)
        else:
            if request.form['filename'] == "Default":
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
    else:
        return render_template('error.html', error="The page has a error please try again")

@app.route('/new_scan', methods=['GET','POST'])
def back_to_main_page():
    return render_template('test.html')
