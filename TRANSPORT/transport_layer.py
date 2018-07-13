


import UDP, threading, time
from Queue import *
from global_var import debug_refresh, debug_flag_TNSP_TX, debug_flag_TNSP_RX, thread_sleep_period
from struct import pack, unpack


class transport_layer:
  def __init__(self,TNSP_options):
    
    self.TNSP_options = TNSP_options
    self.sessions = list()
    
    self.from_network_layer = Queue()
    self.to_network_layer = Queue()
    
    if debug_flag_TNSP_TX or debug_flag_TNSP_TX:
      print self.TNSP_options
    session_ID = 1
    for protocol,options in self.TNSP_options:
      if protocol == 'UDP':
	MSS,source_port,destination_port = options
	self.sessions.append(UDP.UDP(session_ID,MSS,source_port,destination_port))
      session_ID +=1
	
  
  def transmitter(self):
    
    while True:
      
      for session in self.sessions:
	if not session.to_network_layer.empty():
	  self.to_network_layer.put(session.to_network_layer.get())
	else:
	  time.sleep(thread_sleep_period)
  
  
  def receiver(self):
    
    session_ID_pos = (0,4)
    while True:
      
      if not self.from_network_layer.empty():
	tnsp_segment = self.from_network_layer.get()
	tnsp_segment_session_ID = unpack('I',tnsp_segment[session_ID_pos[0]:session_ID_pos[1]])[0]
	
	
	
	for session in self.sessions:
	  if session.session_ID == tnsp_segment_session_ID:
	     session.from_network_layer.put(tnsp_segment)
	     
      else:
	time.sleep(thread_sleep_period)
  
    
  
  
  def run(self):
    threading.Thread(target=self.transmitter).start()
    threading.Thread(target=self.receiver).start()
    
    for session in self.sessions:
      session.run()
    
  