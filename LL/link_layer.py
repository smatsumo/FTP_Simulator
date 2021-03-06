import threading, time
from Queue import *
from global_var import debug_refresh,debug_flag_LL,thread_sleep_period


### import MAC protocols
import Ethernet


class link_layer:
  def __init__(self,LL_options,interface_IP_addresses):
    
    # these options are not given yet but it could include error correction protocols, IEEE 802.11 MAC, etc.
    self.LL_options  = LL_options 
    
    
    self.interface_IP_addresses = interface_IP_addresses
    
    self.mac_protocols = list()
    self.mac_protocols_index = dict()
    
    if debug_flag_LL:
      print self.LL_options
    
    for (protocol,options) in self.LL_options:
      if protocol == 'Ethernet':
	interface_ID = options
	self.mac_protocols.append(Ethernet.Ethernet(interface_IP_addresses[interface_ID]))
	self.mac_protocols_index['Ethernet'] = interface_ID
    
    
    
    
    self.from_network_layer = dict()
    self.to_phy_layer = dict()
    
    self.from_phy_layer = dict()
    self.to_network_layer = dict()
    
    for (intf,mac) in interface_IP_addresses:
      self.from_network_layer[intf] = Queue()
      self.to_phy_layer[mac] = Queue()
      self.from_phy_layer[mac] = Queue()
      self.to_network_layer[intf] = Queue()
     
    self.current_frame_no = 0
  
  def transfer_to_buffer(self,frame,mac_address):
    self.to_phy_layer[mac_address][self.current_frame_no] = frame
    self.current_frame_no +=1
      
  def transmitter(self):
    
    counter = 0
    self.active_mac_protocol = self.mac_protocols_index['Ethernet']
    (intf,mac) = self.mac_protocols[self.active_mac_protocol].interface_MAC_address
    while True:
      
      if not self.from_network_layer[intf].empty():
	
	
	net_datagram = self.from_network_layer[intf].get()
	ll_frame = self.mac_protocols[self.active_mac_protocol].make_frame(net_datagram)
	self.to_phy_layer[mac].put(ll_frame)
	
      else:
	time.sleep(thread_sleep_period)
	
	counter +=thread_sleep_period
	### debug
	if debug_flag_LL and counter % debug_refresh:
	  print "Link Layer -- ", intf, " -- ", mac, " -- "
	  print "Length of self.from_network_layer is : ", self.from_network_layer[intf].qsize()
	  print "Length of self.to_phy_layer is: ", self.to_phy_layer[mac].qsize()
	  
	    
	  
    
  def receiver(self):
    
    counter = 0
    self.active_mac_protocol = self.mac_protocols_index['Ethernet']
    (intf,mac) = self.mac_protocols[self.active_mac_protocol].interface_MAC_address
    while True:
      
      if not self.from_phy_layer[mac].empty():
	
	
	ll_frame = self.from_phy_layer[mac].get()
	net_datagram = self.mac_protocols[self.active_mac_protocol].get_datagram(ll_frame)
	#print len(net_datagram),
	self.to_network_layer[intf].put(net_datagram)
	
	
      else:
	time.sleep(thread_sleep_period)
	
	counter +=thread_sleep_period
	### debug
	if debug_flag_LL and counter % debug_refresh:
	  print "Link Layer -- ", intf, " -- ", mac, " -- "
	  print "Length of self.to_network_layer is : ", self.to_network_layer[intf].qsize()
	  print "Length of self.from_phy_layer is: ", self.from_phy_layer[mac].qsize()
	  
	    
    
    
	
  def run(self):
    threading.Thread(target=self.transmitter).start()
    threading.Thread(target=self.receiver).start()