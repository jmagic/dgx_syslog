
import wx
import logging
import SocketServer
import telnetlib
import time

class SyslogSocketListen(SocketServer.BaseRequestHandler):
 
    def handle(self):
        data = self.request[0].strip()
        print data
        socket = self.request[1]
        print( "%s : " % self.client_address[0], str(data))
        logging.info(str(data))

class MainPanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        self.top_sizer = wx.BoxSizer(wx.VERTICAL)
        
        main_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        
               
        bsizer6 = wx.BoxSizer(wx.VERTICAL)
        
        sbsizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Results"), 
                                                                    wx.VERTICAL)
        self.results = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
                                   wx.DefaultPosition, 
                                   wx.DefaultSize, 
                                   wx.TE_MULTILINE|
                                   wx.TE_READONLY|
                                   wx.HSCROLL)

        self.results.SetMinSize(wx.Size(500, 300))
        
        sbsizer4.Add(self.results, 1, wx.ALL|wx.EXPAND, 5)
    
        bsizer6.Add(sbsizer4, 1, wx.EXPAND, 5)

        self.top_sizer.Add(bsizer6, 1, wx.EXPAND, 5)

        bsizer9 = wx.BoxSizer(wx.HORIZONTAL)

        self.notes = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, 
                        wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        bsizer9.Add(self.notes, 1, wx.ALL, 5)

               
        bsizer6.Add(bsizer9, 0, wx.EXPAND, 5)
        
            
        
        #self.top_sizer.Add(bsizer7, 0, wx.ALIGN_RIGHT, 5)
        
        
        self.SetSizer(self.top_sizer)
        self.Layout()
    
        
        self.Centre(wx.BOTH)
        self.SetPosition((0, 0))




        logging.basicConfig(level=logging.INFO, format='%(message)s', 
                                    datefmt='', filename=LOG_FILE, filemode='a')

       

########################################################################
class MainFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):

        self.title_text = "Starting up"
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, 
                          title=self.title_text, size=(1100, 600))

        self.panel = MainPanel(self)


#----------------------------------------------------------------------
########################################################################
class GenApp(wx.App):

    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    #----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = MainFrame()
        frame.Show()
        return True



def main():

    app = GenApp()
    app.MainLoop()

# Run the program
if __name__ == "__main__":
    LOG_FILE = 'logfile.log'
    HOST, PORT = "0.0.0.0", 514
     
    DGX_IP = '192.168.7.172'
    DGX_SYSTEM = '5002:3:0'
    YOUR_MACHINE_IP = '192.168.7.104'
    YOUR_MACHINE_MAC = 'F4:6D:04:1B:BA:31'
    #'5C:26:0A:48:93:7F'
    try:
        syslog_server = SocketServer.UDPServer((HOST,PORT), SyslogSocketListen)
        syslog_server.serve_forever(poll_interval=0.5)
        main()
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        #telnet_session.write('send_command ' + DGX_SYSTEM + ', \"\'set BCPU_syslog_enabled=OFF\', $0D\" \r')
        print " Shutting down debugging."



