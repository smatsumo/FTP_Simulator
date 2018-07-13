# define applicaiton layer classess 

# define ftp class

#from bitstring import BitArray
import threading,time,sys
from Queue import *

from global_var import debug_flag_APP, thread_sleep_period
from struct import pack, unpack

class FTP:
  def __init__(self,session_ID,filename,mode):
      # define necessary private variables for this class
      # define buffer to send FTP data to transport layer
      self.to_transport_layer = Queue()
      
      #define buffer to receive data from transport layer
      self.from_transport_layer = Queue()
      
      # make a local variables for IP and port numbers
      # IP and port numbers will be passed down to the transport_layer
     
      
      self.tx_line_number = 0
      self.rx_line_number = -1
      self.session_ID = session_ID
      
      self.mode = mode
      self.filename = filename
      if self.mode == 'TX':
	self.ftp_file = open(self.filename,'r')
      elif self.mode == 'RX':
	self.ftp_file = open(self.filename,'w')
      
      
            
  def transmitter(self):
      # define transmitter function
      # this function read from a file <given by filename> line by line
      # and insert the data to buffer for transport layer
      
      # open a file < we assume the file is ASCII
      
      
      # read from a file line-by-line and store it in the buffer for 
      
      
      
      for line in self.ftp_file:
	FTP_payload = str()
	# line number
	FTP_payload+= pack('I',self.tx_line_number)
	# payload
	for ch in line:
	  FTP_payload += pack('c',ch)
	  
	self.to_transport_layer.put(FTP_payload)
	self.tx_line_number+=1
      
       
      
      ### debug
      if debug_flag_APP:
	print "session_ID is: ", self.session_ID
	print "total lines in file: ", self.filename, " is ", self.tx_line_number
  
  
  
  
  
  
  def process_payload(self,app_payload):
    
    line_number = unpack('I',app_payload[:4])[0]
    sys.stderr.write(str(line_number) + ',')
    data = str()
    for ch in app_payload[4:]:
      data += unpack('c',ch)[0]
    if line_number == self.rx_line_number + 1:
      self.rx_line_number +=1
      return (True,data)
    else:
      return (False,data)
    
  
  
  
  
  
  
  
  def receiver(self):
    # define a receiver function
    # this function gets the segmented packets from the transport layer buffer and 
    # create a file < we assume an ASCII file> specified by filename 
    
    # open a file to write into
   
    
    while True:
      #sys.stderr.write(str(self.from_transport_layer.qsize()))
      if not self.from_transport_layer.empty():
	
	app_payload = self.from_transport_layer.get()
	(suc,data) = self.process_payload(app_payload)
	if self.ftp_file.closed:
	  self.ftp_file = open(self.filename,'a')
	
	if not suc:
	  self.ftp_file.write('Missing Line')
	#print data
	self.ftp_file.write(data)
	self.ftp_file.close()
	  
      else:
	time.sleep(thread_sleep_period)
	
      
      
      
  def run(self):
    if self.mode == 'TX':
      threading.Thread(target=self.transmitter).start()
    elif self.mode == 'RX':
      threading.Thread(target=self.receiver).start()
    
      
	
	