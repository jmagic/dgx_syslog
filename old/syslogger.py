DGX_IP = "192.168.7.91"
YOUR_COMPUTER_IP = "192.168.7.104"
YOUR_COMPUTER_MAC = "f4:6d:04:1b:ba:31"

LOG_FILE = 'dgx.log'
HOST, PORT = "localhost", 514

import telnetlib 
import logging
import SocketServer
import pickle
import os

#setup syslog logging via telnet
'''telnet_session = telnetlib.Telnet(DGX_IP, 23, 5)
intro = telnet_session.read_very_eager().split()
telnet_session.write('send_command 5002:3:0, \"$03\" \r')
telnet_session.write('send_command 5002:3:0, \"\'set BCPU1_syslog_enabled=ON\', $0D\" \r')
telnet_session.write('send_command 5002:3:0, \"\'set BCPU1_syslog_server_ip_address=' + YOUR_COMPUTER_IP + '\', $0D\" \r')
telnet_session.write('send_command 5002:3:0, \"\'set BCPU1_syslog_server_mac_address=' + YOUR_COMPUTER_MAC + '\', $0D\" \r')'''
print 'before logging'
logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')
print 'logging started'
 
class SyslogUDPHandler(SocketServer.BaseRequestHandler):
 
    def handle(self):
        print 'in handle'
        #print self.request[0]
        #path = os.path.expanduser('~\\Documents\\pysyslog\\')
        #pickle.dump(self.request[0], open( 'test.pkl', 'wb'))
        data = self.request[0].strip()
        socket = self.request[1]
        print( "%s : " % self.client_address[0], data)
        logging.info(str(data))

 
if __name__ == "__main__":
    try:
        server = SocketServer.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("exit")