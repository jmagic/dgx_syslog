
LOG_FILE = 'yourlogfile.log'
HOST, PORT = "0.0.0.0", 514
 
DGX_IP = '192.168.2.12'
YOUR_MACHINE_IP='192.168.2.225'
YOUR_MACHINE_MAC='5C:26:0A:48:93:7F'

import logging
import SocketServer
import telnetlib


telnet_session = telnetlib.Telnet(DGX_IP, 23, 5)
#print "starting telnet", telnet_session.read_very_eager()
telnet_session.write('send_command 5002:3:2, \"$03\" \r')
#print telnet_session.read_very_eager()
telnet_session.write('send_command 5002:3:2, \"\'set BCPU_syslog_enabled=ON\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'set BCPU_syslog_server_ip_address=' + YOUR_MACHINE_IP + '\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'set BCPU_syslog_server_mac_address=' + YOUR_MACHINE_MAC + '\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'su\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'enova\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'12amx34\', $0D\" \r') 
telnet_session.write('send_command 5002:3:2, \"\'remote BCPU1\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'|\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'d\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'1\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'1\', $0D\" \r')
telnet_session.write('send_command 5002:3:2, \"\'a\', $0D\" \r')

logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')
 
class SyslogUDPHandler(SocketServer.BaseRequestHandler):
 
    def handle(self):
        data = self.request[0].strip()
        print data
        socket = self.request[1]
        print( "%s : " % self.client_address[0], str(data))
        logging.info(str(data))
 
if __name__ == "__main__":
    try:
        server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        telnet_session.write('send_command 5002:3:2, \"\'set BCPU_syslog_enabled=OFF\', $0D\" \r')
        print ("Crtl+C Pressed. Shutting down debugging.")