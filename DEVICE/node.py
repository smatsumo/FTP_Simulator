import sys,  threading
from itertools import izip



from application_layer import *
from transport_layer import *
from network_layer import *
from  link_layer import *
from physical_layer import *
from global_var import _connect



class end_user(threading.Thread):
  def __init__(self,node_ID,options):
    threading.Thread.__init__(self)
    
   
    ### define node's protocols at different layers
    
    
   
    self.node_options = options
    self.interface_IP_addresses = self.node_options['IFCONFIG']
    self.APP = application_layer(self.node_options['sessions']['APP'])
    self.TNSP = transport_layer(self.node_options['sessions']['TNSP'])
    
    if len(self.node_options['NET']) == 0 or len(self.node_options['LL']) == 0 or len(self.node_options['PHY']) == 0:
      print "Node NET/LL/PHY definitions missig..exiting"
      exit()
      
    self.NET = network_layer(self.node_options['NET'],self.interface_IP_addresses)
    self.LL = link_layer(self.node_options['LL'],self.interface_IP_addresses)
    self.PHY = physical_layer(self.node_options['PHY']) 
    
    
    
    
  def run(self):
    
    
    
     
    self.APP.run()
    self.TNSP.run()
    self.NET.run()
    self.LL.run()
    self.PHY.run()
     
    ### setup connections
    
    for app_session,tnsp_session in izip(self.APP.sessions,self.TNSP.sessions):
     threading.Thread(target=_connect, args=(app_session.to_transport_layer,tnsp_session.from_application_layer)).start()
     threading.Thread(target=_connect, args=(tnsp_session.to_application_layer,app_session.from_transport_layer)).start()
    
    threading.Thread(target=_connect, args=(self.TNSP.to_network_layer,self.NET.from_transport_layer)).start()
    threading.Thread(target=_connect, args=(self.NET.to_transport_layer, self.TNSP.from_network_layer)).start()
    
    for (intf,mac) in self.interface_IP_addresses:
      threading.Thread(target=_connect, args=(self.NET.to_link_layer[intf],self.LL.from_network_layer[intf])).start()
      threading.Thread(target=_connect, args=(self.LL.to_network_layer[intf],self.NET.from_link_layer[intf])).start()
      
    for (intf,mac) in self.interface_IP_addresses:
      threading.Thread(target=_connect, args=(self.LL.to_phy_layer[mac],self.PHY.from_link_layer[mac])).start()
      threading.Thread(target=_connect, args=(self.PHY.to_link_layer[mac],self.LL.from_phy_layer[mac])).start()  
    
      
      
      
      
      
      
      
      
    