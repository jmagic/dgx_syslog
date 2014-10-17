"""A SYS logger that listens for  messages"""

from threading import Thread
import socket
from pydispatch import dispatcher
import wx
import logging
import SocketServer
import telnetlib
import time
import socket
import uuid



########################################################################
class SyslogUDPHandler(SocketServer.BaseRequestHandler):
 
    def handle(self):
        data = self.request[0].strip()
        #print "data"
        #dispatcher.send(signal="Incoming Data", sender=data)
        socket = self.request[1]
        #print
        dispatcher.send(signal="Incoming Data", 
                        sender=( "%s : " % self.client_address[0], str(data)))
        #logging.info(str(data))

class SysListener(Thread):
    """The sys listener thread"""

    #----------------------------------------------------------------------
    def __init__(self, parent, HOST, PORT):
        """Init Worker Thread Class."""

        self.host = HOST
        self.port = PORT
        self.parent = parent
        Thread.__init__(self)

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        try:
            server = SocketServer.UDPServer((self.host, self.port), SyslogUDPHandler)
            server.serve_forever(poll_interval=0.5)
        except Exception as error:
            dispatcher.send(signal="Incoming error", sender=(error))
        
        #txtHandler = CustomConsoleHandler(logText)
        #self.logger.addHandler(txtHandler)
        
        #logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', 
        #             
        #            filename=LOG_FILE, filemode='a')

        #send the processed packet to the main loop
        #wx.CallAfter(self.send_info, (hostname, mac_address, 
        #                                                ip_address))



    #----------------------------------------------------------------------
    def send_info(self, info):
        """
        Send data to GUI
        """
        dispatcher.send(signal="Incoming Packet", sender=info)

########################################################################

