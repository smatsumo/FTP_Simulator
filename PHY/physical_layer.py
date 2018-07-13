import socket, threading, time


from Queue import *
from global_var import debug_refresh,debug_flag_PHY,thread_sleep_period


import socket_phy as SPHY

class physical_layer:
  
  def __init__(self,PHY_options):
    
       
    self.PHY_options = PHY_options
    self.phy_medium = dict()
    self.from_link_layer = dict()
    self.to_link_layer = dict()
   
    
    
    for (medium,options) in self.PHY_options:
      
      if medium == 'socket_phy': # for socket_phy mac + 1 is always rx port
	(ID,ip,mac,tx,rx) = options
	self.from_link_layer[mac] = Queue()
	self.to_link_layer[mac] = Queue()
	self.phy_medium[ID] = SPHY.SPHY(ID,mac,ip,tx,rx)
	
  def transmitter(self):
    
    
    counter = 0
    ID = self.active_mac_protocol = 0 # for now we use a defult interface
    mac = self.phy_medium[self.active_mac_protocol].mac
    while True:
      
      if not self.from_link_layer[mac].empty():
	
	
	ll_frame = self.from_link_layer[mac].get()
	### PHY Encapsulation
	### Under Construction
	phy_frame = ll_frame
	### PHY Encapsulation
	
	
	self.phy_medium[self.active_mac_protocol].send(phy_frame)
	
	
      else:
	time.sleep(thread_sleep_period)
	
	counter +=thread_sleep_period
	### debug
	if debug_flag_PHY and counter % debug_refresh:
	  print "PHY Layer -- ", ID , " -- ", mac, " -- "
	  print "Length of self.from_link_layer is : ", self.from_link_layer[mac].qsize()
	  print "frames to send: ", self.phy_medium[ID].tx_buffer.qsize()
	  
    
    
  
  def receiver(self):
    
    counter = 0
    ID = self.active_mac_protocol = 0 # for now we use a defult interface
    mac = self.phy_medium[self.active_mac_protocol].mac
    while True:
      
      if self.phy_medium[self.active_mac_protocol].has_data():
	
	
	phy_frame = self.phy_medium[self.active_mac_protocol].receive()
	
	### PHY Decapsulation
	### Under Construction
	ll_frame = phy_frame
	### PHY Decapsulation
	
	#print len(phy_frame),
	self.to_link_layer[mac].put(ll_frame)
	
      else:
	time.sleep(thread_sleep_period)
	
	counter +=thread_sleep_period
	### debug
	if debug_flag_PHY and counter % debug_refresh:
	  print "PHY Layer -- ", ID , " -- ", mac, " -- "
	  print "Length of self.from_link_layer is : ", self.to_link_layer[mac].qsize()
	  print "frames received: ", self.phy_medium[ID].rx_buffer.qsize()
	
    
    
    
	
	
  def run(self):
     threading.Thread(target=self.transmitter).start()
     threading.Thread(target=self.receiver).start()
    
    
    
