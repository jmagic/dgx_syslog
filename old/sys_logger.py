
LOG_FILE = 'yourlogfile.log'
HOST, PORT = "0.0.0.0", 514
 
DGX_IP = '192.168.7.77'
DGX_SYSTEM = '5002:3:0'
#YOUR_MACHINE_IP='192.168.7.134'
#YOUR_MACHINE_MAC='F4:6D:04:1B:BA:31'
#'5C:26:0A:48:93:7F'

import logging
import SocketServer
import telnetlib
import time
import socket
import uuid

def slow_down():
    time.sleep(1)


hostname = socket.gethostname()
YOUR_MACHINE_IP = socket.gethostbyname(hostname)
YOUR_MACHINE_MAC = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

print "IP: ", YOUR_MACHINE_IP
print "MAC: ", YOUR_MACHINE_MAC

telnet_session = telnetlib.Telnet(DGX_IP, 23, 5)
print "starting telnet"
print telnet_session.read_until('Welcome', 5)
#print telnet_session.read_all()
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"$03\" \r')
slow_down()
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'set BCPU_syslog_enabled=ON\', $0D\" \r')
slow_down()
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'set BCPU_syslog_server_ip_address=' + YOUR_MACHINE_IP + '\', $0D\" \r')
slow_down()
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'set BCPU_syslog_server_mac_address=' + YOUR_MACHINE_MAC + '\', $0D\" \r')
#print telnet_session.read_until('mac_address', 5)
print "set of syslog complete"

#print telnet_session.read_very_eager()
#raw_input()
slow_down()
'''
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'su\', $0D\" \r')
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'enova\', $0D\" \r')
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'12amx34\', $0D\" \r') 
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'remote BCPU1\', $0D\" \r')
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'|\', $0D\" \r')
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'d\', $0D\" \r')
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'1\', $0D\" \r')
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'1\', $0D\" \r')
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'b\', $0D\" \r')
print telnet_session.read_very_eager()'''

logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', 
                    filename=LOG_FILE, filemode='a')
 
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
        telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'set BCPU_syslog_enabled=OFF\', $0D\" \r')
        print ("Crtl+C Pressed. Shutting down debugging.")