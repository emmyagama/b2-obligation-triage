"""B2 core. B2_OFFLINE also blocks socket-level network connections."""
import os
if os.environ.get('B2_OFFLINE') == '1':
    import socket
    _connect = socket.socket.connect
    _connect_ex = socket.socket.connect_ex
    def _deny_connect(self, address):
        if self.family in (socket.AF_INET, socket.AF_INET6):
            raise RuntimeError('B2_OFFLINE prohibits HTTP and TCP/IP')
        return _connect(self,address)
    def _deny_connect_ex(self, address):
        if self.family in (socket.AF_INET, socket.AF_INET6):
            raise RuntimeError('B2_OFFLINE prohibits HTTP and TCP/IP')
        return _connect_ex(self,address)
    socket.socket.connect = _deny_connect
    socket.socket.connect_ex = _deny_connect_ex
