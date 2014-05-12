DGX_IP = '192.168.7.92'
DGX_SYSTEM = '5002:3:0'
YOUR_MACHINE_IP='192.168.7.104'
YOUR_MACHINE_MAC='F4:6D:04:1B:BA:31'
#'5C:26:0A:48:93:7F'

delay_time = 12

import logging
import SocketServer
import telnetlib
import time

telnet_session = telnetlib.Telnet(DGX_IP, 23, 5)
print telnet_session.read_until('>', 5)
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"$03\"\r')
print 'send_command ' + DGX_SYSTEM + ', \"$03\"\r'
time.sleep(delay_time)
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'su\', $0D, \
                                                         \'enova\', $0D, \
                                                         \'12amx34\', $0D\"\r')
#print 'send_command ' + DGX_SYSTEM + ', \"\'su\', $0D\"\r'
#time.sleep(delay_time)
#telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'enova\', $0D\"\r')
#print 'send_command ' + DGX_SYSTEM + ', \"\'enova\', $0D\"\r'
#time.sleep(delay_time)
#telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'12amx34\', $0D\"\r') 
#print 'send_command ' + DGX_SYSTEM + ', \"\'12amx34\', $0D\"\r'
time.sleep(delay_time)
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'remote BCPU1\', $0D\"\r')
print 'send_command ' + DGX_SYSTEM + ', \"\'remote BCPU1\', $0D\"\r'
time.sleep(delay_time)
#telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'|\', $0D\"\r')
#print 'send_command ' + DGX_SYSTEM + ', \"\'|\', $0D\"\r'
#time.sleep(delay_time)
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'d\', $0D\"\r')
print 'send_command ' + DGX_SYSTEM + ', \"\'d\', $0D\"\r'
time.sleep(delay_time)
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'1\', $0D\"\r')
print 'send_command ' + DGX_SYSTEM + ', \"\'3\', $0D\"\r'
time.sleep(delay_time)
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'1\', $0D\"\r')
time.sleep(delay_time)
telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'b\', $0D\"\r')
time.sleep(delay_time)


telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'bcs\', $0D\"\r')
print 'send_command ' + DGX_SYSTEM + ', \"\'bcs\', $0D\"\r'
time.sleep(delay_time)
print "done"