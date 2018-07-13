import RIP
import threading, time
from Queue import *
from global_var import debug_refresh,debug_flag_NET_TX, debug_flag_NET_RX, thread_sleep_period



class network_layer:
  def __init__(self,NET_options,interface_IP_addresses):
    
    self.NET_options = NET_options
    
    self.routing_protocols = list()
    self.routing_protocols_index = dict()
    
    if debug_flag_NET_TX or debug_flag_NET_RX:
      print self.NET_options
    counter = 0
    for (protocol,options) in self.NET_options:
      if protocol == 'RIP':
	self.routing_protocols.append(RIP.RIP(interface_IP_addresses))
	self.routing_protocols_index['RIP'] = counter
      counter +=1
    
    
    
    self.from_transport_layer = Queue()
    self.to_transport_layer = Queue()
    
    self.to_link_layer = dict()
    self.from_link_layer = dict()
    
    
    for (intf,mac) in interface_IP_addresses:
      self.to_link_layer[intf] = Queue()
      self.from_link_layer[intf] = Queue()
      
    self.interface_IP_addresses = interface_IP_addresses
	
  
  def transmitter(self):
    
    counter = 0
    self.active_routing_protocol = self.routing_protocols_index['RIP']
    while True:
      
      if not self.from_transport_layer.empty():
	
	tnsp_segment = self.from_transport_layer.get()
	net_datagram = self.routing_protocols[self.active_routing_protocol].make_datagram(tnsp_segment)
	intf = self.routing_protocols[self.active_routing_protocol].get_interface_IP_address()
	self.to_link_layer[intf].put(net_datagram)
      else:
	time.sleep(thread_sleep_period)
	
	counter +=1
	### debug
	if debug_flag_NET_TX and counter % debug_refresh:
	  print "Length of self.from_transport_layer is : ", self.from_transport_layer.qsize()
	  print "Length of network interface queues are: "
	  for (intf,mac) in self.interface_IP_addresses:
	     print " -- ", intf, " -- ", self.to_link_layer[intf].qsize()
	  
	 
  
  def receiver(self):
    
    counter = 0
    self.active_routing_protocol = self.routing_protocols_index['RIP']
    intf = self.routing_protocols[self.active_routing_protocol].get_interface_IP_address()
    while True:
      
      if not self.from_link_layer[intf].empty():
	
	
	net_datagram = self.from_link_layer[intf].get()
	tnsp_segment = self.routing_protocols[self.active_routing_protocol].get_segment(net_datagram)
	#print len(tnsp_segment),
	self.to_transport_layer.put(tnsp_segment)
      
      else:
	time.sleep(thread_sleep_period)
	
	counter += thread_sleep_period
	### debug
	if debug_flag_NET_RX and counter % debug_refresh:
	  print "Length of self.to_transport_layer is : ", self.from_transport_layer.qsize()
	  print "Length of LL interface queues are: "
	  for (intf,mac) in self.interface_IP_addresses:
	     print " -- ", intf, " -- ", self.from_link_layer[intf].qsize()
	  
    
  
  
  def run(self):
    
    threading.Thread(target=self.transmitter).start()
    threading.Thread(target=self.receiver).start()
    
    
    
    
  