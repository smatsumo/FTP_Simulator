import threading, time 
from Queue import *


debug_refresh = 20 
thread_sleep_period = 0.01 # unit is sec

debug_flag_APP = False
debug_flag_TNSP_TX = False
debug_flag_TNSP_RX = False
debug_flag_NET_TX = False
debug_flag_NET_RX = False
debug_flag_LL = False
debug_flag_PHY = False


threadLock = threading.Lock()

def _connect(in_buffer,out_buffer):
  
  #if type(in_buffer) != Queue:
    #print "EROOR in _connect: in_buffer type should be Queue"
    #exit()
  #if type(out_buffer) != Queue:
    #print "EROOR in _connect: in_buffer type should be Queue"
    #exit()
  
  while True:
    if not in_buffer.empty():
      threadLock.acquire()
      
      pkt = in_buffer.get()
      out_buffer.put(pkt)
      
      threadLock.release()
       #print "tranfered.."
    else:
      time.sleep(0.1)
      #print "wait.." 