import socket


class create_Socket:
    """class of creating a socket to preform a scan of the volatile ports"""
    def __init__(self, host):
        self.host = host


    def TCPportscan(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in range(1,65535):
            addr = (self.host, port)
            try:
                result = s.connect(addr)
                if result == 0:
                    print('TCP port ' + str(port) + ' is open')
            except InterruptedError:
                print('Connection has been interrupted')
            except:
                print('Something else went wrong')


    def UDPportscan(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.settimeout(5)
        for port in range(1,65535):
            addr = (self.host, port)
            s.sendto(b"H",addr)
            try:
                data = s.recvfrom(4096)
                if data[0] != "":
                    print("The following data hase been received from " + data[1] + " : " + data[1])
            except ConnectionResetError:
                print("Connection reset from host at: " + self.host + ":" + str(port))
            except socket.timeout:
                print("No response from the host at: " + self.host + ":" + str(port))

    
