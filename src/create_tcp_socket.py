import socket


class create_Socket:
    """class of creating a socket to preform a scan of the volatile ports"""
    def __init__(self, host):
        self.host = host


    def TCPportscan(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in range(1,65535):
            addr = (self.host, port)
            result = s.connect_ex(addr)
            if result == 0:
                print('TCP port ' + str(port) + ' is open')
