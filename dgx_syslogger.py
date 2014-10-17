"""Listens for syslog events on a DGX"""
import os
import telnetlib
import time
import socket
import wx
import sys_thread
from pydispatch import dispatcher
import dgx_gui
import ConfigParser


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
        self.path = os.path.expanduser(
                                    '~\\Documents\\DGX_Syslog\\')
        self.read_config_file()
        #self.ip_address = "192.168.7.114"
        #self.mac_address = "5C:26:0A:48:93:7F"

        

        dispatcher.connect(self.incoming_data, 
                           signal="Incoming Data", 
                           sender=dispatcher.Any)
        dispatcher.connect(self.incoming_error, 
                           signal="Incoming error", 
                           sender=dispatcher.Any)
        

        #self.window = dgx_gui.ipdialog(self)
        #self.window.Show()
        self.get_computer_ip_and_mac()
        #while not self.dgx_ip_valid:
        self.get_dgx_ip_address()

        # Create syslog listening thread
        sys_listener = sys_thread.SysListener(self, HOST, PORT)
        sys_listener.setDaemon(True)
        sys_listener.start()
        print "started listening"


    def read_config_file(self):
        """Reads the config file"""
        config = ConfigParser.RawConfigParser()
        try:  # read the settings file
            config.read((self.path + "settings.txt"))
            self.ip_address = (config.get('Settings', 
                                  'Computer IP'))
            self.mac_address = (config.get('Settings',
                                  'Computer MAC'))
            self.dgx_ip = (config.get('Settings', 
                                 'DGX IP'))

            
        except (ConfigParser.Error, IOError):   
            # Make a new settings file, because we couldn't read the old one
            self.create_config_file()
            self.read_config_file()
        return

    def create_config_file(self):
        """Creates a new config file"""
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        try:
            os.remove(self.path + 'settings.txt')
        except OSError:
            pass
        with open((self.path + "settings.txt"), 'w') as config_file:
            config_file.write("")
        config = ConfigParser.RawConfigParser()
        config.add_section('Settings')
        config.set('Settings', 'Computer IP', '')
        config.set('Settings', 'Computer MAC', '')
        config.set('Settings', 'DGX IP', '')
        with open((self.path + "settings.txt"), 'w') as configfile:
            config.write(configfile)

    def write_config_file(self):
        """Update values in config file"""
        config = ConfigParser.RawConfigParser()
        config.read((self.path + "settings.txt"))
        config.set('Settings', 'Computer IP', self.ip_address)
        config.set('Settings', 'Computer MAC', self.mac_address)
        config.set('Settings', 'DGX IP', self.dgx_ip)
        with open((self.path + "settings.txt"), 'w') as configfile:
            config.write(configfile)


    def on_enable_logging( self, event ):
        "Sends telnet commands to setup syslog"
        dlg = dgx_gui.connection_progress(self)
        dlg.Show()
        #we have 5 stages
        dlg.progress_bar.SetRange(5)
        dlg.progress_text.SetLabel('Connecting to Telnet')
        dlg.progress_bar.SetValue(1)

        telnet_session = telnetlib.Telnet(self.dgx_ip, 23, 5)
        telnet_session.read_until('Welcome', 5)

        telnet_session.write('send_command ' + self.dgx_system + ', \"$03\" \r')
        dlg.progress_bar.SetValue(2)
        dlg.progress_text.SetLabel('Breaking into DGX shell')

        self.slow_down()
        
        telnet_session.write('send_command ' + self.dgx_system + 
                             ', \"\'set BCPU_syslog_server_ip_address=' + 
                             self.ip_address + '\', $0D\" \r')
        dlg.progress_text.SetLabel('Setting Server IP')
        dlg.progress_bar.SetValue(3)
        self.slow_down()
        
        telnet_session.write('send_command ' + self.dgx_system + 
                             ', \"\'set BCPU_syslog_server_mac_address=' +
                             self.mac_address + '\', $0D\" \r')
        dlg.progress_text.SetLabel('Setting Server MAC')
        dlg.progress_bar.SetValue(4)
        self.slow_down()

        telnet_session.write('send_command ' + self.dgx_system + 
                                 ', \"\'set BCPU_syslog_enabled=ON\', $0D\" \r')
        dlg.progress_text.SetLabel('Enable Syslog')
        dlg.progress_bar.SetValue(5)
        self.slow_down()
        dlg.Destroy()

    
    def on_disable_logging( self, event ):
        "Sends telnet commands to disable syslog"
        dlg = dgx_gui.connection_progress(self)
        dlg.Show()
        #we have 5 stages
        dlg.progress_bar.SetRange(5)
        dlg.progress_text.SetLabel('Connecting to Telnet')
        dlg.progress_bar.SetValue(1)
        telnet_session = telnetlib.Telnet(self.dgx_ip, 23, 5)
        telnet_session.read_until('Welcome', 5)
        



        telnet_session.write('send_command ' + self.dgx_system + ', \"$03\" \r')
        dlg.progress_text.SetLabel('Breaking into DGX shell')
        dlg.progress_bar.SetValue(2)
        self.slow_down()

        
        telnet_session.write('send_command ' + self.dgx_system + 
                                 ', \"\'set BCPU_syslog_enabled=OFF\', $0D\" \r')
        dlg.progress_text.SetLabel('Disabling syslog')
        dlg.progress_bar.SetValue(3)
        self.slow_down()
        
        telnet_session.write('send_command ' + self.dgx_system + 
                             ', \"\'set BCPU_syslog_server_ip_address=' + 
                             '0.0.0.0\', $0D\" \r')
        dlg.progress_text.SetLabel('Setting server IP to 0.0.0.0')
        dlg.progress_bar.SetValue(4)
        self.slow_down()
        
        telnet_session.write('send_command ' + self.dgx_system + 
                             ', \"\'set BCPU_syslog_server_mac_address=' +
                             '00:00:00:00:00:00\', $0D\" \r')
        dlg.progress_text.SetLabel('Setting server MAC to 00:00:00:00:00:00')
        dlg.progress_bar.SetValue(5)
        self.slow_down()

        dlg.Destroy()



    def get_dgx_ip_address(self):
        """Gets DGX IP information for session"""
        dlg = dgx_gui.ipdialog(self)
        dlg.dgx_ip_text.SetLabel(self.dgx_ip)
        if dlg.ShowModal() == wx.ID_OK:
            if(self.is_valid_ipv4(dlg.dgx_ip_text.GetValue())):
                self.dgx_ip = dlg.dgx_ip_text.GetValue()
                self.write_config_file()


    def get_computer_ip_and_mac(self):
        """Gets the ip and mac of the computer"""
        dlg = dgx_gui.local_ip_and_mac(self)
        dlg.computer_ip_text.SetLabel(self.ip_address)
        dlg.computer_mac_text.SetLabel(self.mac_address)
        if dlg.ShowModal() == wx.ID_OK:
            if(self.is_valid_ipv4(dlg.computer_ip_text.GetValue())):
                self.ip_address = str(dlg.computer_ip_text.GetValue())
                self.mac_address = str(dlg.computer_mac_text.GetValue())
                self.write_config_file()




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

    def incoming_error(self, sender):
        """Print error and exit"""
        dlg = wx.MessageDialog(self.parent,
           message=('I\'ve had a probelm: ' + str(sender)),
           caption='Errors detected',
           style=wx.OK)
        dlg.ShowModal()
        self.Destroy()




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