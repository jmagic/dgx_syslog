import logging
import SocketServer
import telnetlib
import time
import socket
import uuid
import wx
import sys_thread
from pydispatch import dispatcher
import dgx_gui


class DGXFrame( dgx_gui.DGXFrame ):
    def __init__( self, parent ):
        dgx_gui.DGXFrame.__init__( self, parent )
    
        #To do ... 
        #Set focus before writing
        #interpert logs properly
        #
        #ask for DGX IP and system number
        self.parent = parent
        self.dgx_ip = '' #
        self.dgx_system = '5002:3:0'
        HOST, PORT = "0.0.0.0", 514
        self.hostname = ''  #socket.gethostname()
        self.ip_address = '' # socket.gethostbyname(self.hostname)
        self.mac_address = '' #.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
        self.dgx_ip_valid = False
        self.ip_address = "192.168.7.114"
        self.mac_address = "5C:26:0A:48:93:7F"

        

        dispatcher.connect(self.incoming_data, 
                           signal="Incoming Data", 
                           sender=dispatcher.Any)
        

        #self.window = dgx_gui.ipdialog(self)
        #self.window.Show()
        while not self.dgx_ip_valid:
            self.get_dgx_ip_address()

        # Create syslog listening thread
        sys_listener = sys_thread.SysListener(self, HOST, PORT)
        sys_listener.setDaemon(True)
        sys_listener.start()
        print "started listening"

        # Handlers for MainFrame events.
    def on_enable_logging( self, event ):
        "Sends telnet commands to setup syslog"
        telnet_session = telnetlib.Telnet(self.dgx_ip, 23, 5)
        telnet_session.read_until('Welcome', 5)
        print 'connected via telnet'
        telnet_session.write('send_command ' + self.dgx_system + ', \"$03\" \r')
        self.slow_down()
        
        telnet_session.write('send_command ' + self.dgx_system + 
                             ', \"\'set BCPU_syslog_server_ip_address=' + 
                             self.ip_address + '\', $0D\" \r')
        self.slow_down()
        
        telnet_session.write('send_command ' + self.dgx_system + 
                             ', \"\'set BCPU_syslog_server_mac_address=' +
                             self.mac_address + '\', $0D\" \r')
        self.slow_down()

        telnet_session.write('send_command ' + self.dgx_system + 
                                 ', \"\'set BCPU_syslog_enabled=ON\', $0D\" \r')
        self.slow_down()
        
        #telnet_session.write('reboot \r')
        #print "system will now reboot"


    
    def on_disable_logging( self, event ):
        "Sends telnet commands to disable syslog"
        telnet_session = telnetlib.Telnet(self.dgx_ip, 23, 5)
        telnet_session.read_until('Welcome', 5)
        print 'connected via telnet'
        telnet_session.write('send_command ' + self.dgx_system + ', \"$03\" \r')
        self.slow_down()
        
        telnet_session.write('send_command ' + self.dgx_system + 
                                 ', \"\'set BCPU_syslog_enabled=OFF\', $0D\" \r')
        self.slow_down()
        
        telnet_session.write('send_command ' + self.dgx_system + 
                             ', \"\'set BCPU_syslog_server_ip_address=' + 
                             '0.0.0.0\', $0D\" \r')
        self.slow_down()
        
        telnet_session.write('send_command ' + self.dgx_system + 
                             ', \"\'set BCPU_syslog_server_mac_address=' +
                             '00:00:00:00:00:00\', $0D\" \r')
        self.slow_down()
        #telnet_session.write('reboot \r')
        #print "system will now reboot"


    def get_dgx_ip_address(self):
        """Gets DGX IP information for session"""
        dlg = wx.TextEntryDialog(
                self, 'What is the IP of the DGX?',
                'Please enter DGX IP', '192.168.7.177')
        if dlg.ShowModal() == wx.ID_OK:
            if(self.is_valid_ipv4(dlg.GetValue())):
                self.dgx_ip = dlg.GetValue()
                self.dgx_ip_valid = True
        dlg.Destroy()

    def is_valid_ipv4(self, ip):
        """Validates IPv4 addresses."""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def incoming_data(self, sender):
        #print "Sender: ", sender
        self.text_area.SetInsertionPointEnd()
        self.text_area.WriteText(sender[1] + "\n")

    def send_BCPU_command(self):
        #dialog to show 
        pass

    def setup_syslog(self, _):
        "Sets up syslog on the DGX"
        dlg = wx.MessageDialog(self.parent,
           message=('Configure DGX to send syslogs to IP: ' + self.ip_address +
                    ' and MAC: ' + self.mac_address),
           caption='Verify IP and MAC',
           style=wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
                self.config_syslog()




    def slow_down(self):
        "time delay"
        time.sleep(2)


########################################################################
class GenApp(wx.App):

    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    #----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = DGXFrame(None)
        
        frame.Show()
        return True

#----------------------------------------------------------------------
def main():

    app = GenApp()

    app.MainLoop()

# Run the program
if __name__ == "__main__":
    main()