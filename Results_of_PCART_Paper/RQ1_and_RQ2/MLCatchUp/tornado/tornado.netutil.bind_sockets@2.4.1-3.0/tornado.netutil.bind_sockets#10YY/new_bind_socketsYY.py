import tornado.netutil
import socket
sockets = tornado.netutil.bind_sockets(8888, '0.0.0.0', socket.AF_UNSPEC, 128, flags=None)