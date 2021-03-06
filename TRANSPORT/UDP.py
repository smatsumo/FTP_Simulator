
# run this with python3




# This function defines necessary classes for the transport layer


# This class implements UDP protocol at the transport layer



# we use md5 library for checksum
import md5, math, time, threading, sys
from Queue import *
# use bitarray to convert sequence of bits to bytes
#from bitstring import BitArray
# BitArray().tobytes() converts sequence of bits to bytes
# BitArray().bin converts bytes to sequence of bits
from global_var import debug_refresh, debug_flag_TNSP_TX, debug_flag_TNSP_RX, thread_sleep_period
from struct import pack, unpack


# UDP_payload: data content for the applicaiton layer

class UDP:
  def __init__(self,session_ID,MSS,source_port,destination_port):
    # define private variables here
    
    #define a buffer to store UDP segments to send to the network layer
    self.to_network_layer = Queue()
    
    # define a buffer that stored datagrams provided by the network layer
    self.from_network_layer = Queue()
    
    # define a buffer to store concantinated packets into data payload to send to the applicaiton layer
    self.to_application_layer = Queue()
    
    # define a buffer to get data payload from application layer to convert them into UDP segments
    self.from_application_layer = Queue()
    
    # define a maximum segment size MSS, source_port and destination_port
    self.MSS = MSS
    
    # convert source_port and destination_port to binary format
    self.source_port = pack('I',source_port)
    self.destination_port = pack('I',destination_port)
    self.current_segment_no = 0
    self.session_ID = session_ID
    
    
    # field_pos is the position of the beginig of each field
    self.field_pos = dict()
    self.field_pos['session_ID'] = (0,4)
    self.field_pos['segment_no'] = (4,8)
    self.field_pos['source_port'] = (8,12)
    self.field_pos['destination_port'] = (12,16)
    self.field_pos['reference_byte' ] = (16,17)
    self.field_pos['length'] = (17,21)
    self.field_pos['app_payload']= (21,21 + self.MSS)
    self.field_pos['crc'] = (21 + self.MSS,37 + self.MSS)
    
    
    # temporary buffer used to concantinate segments
    self.payload_recovery_buffer = dict()
    
  def make_UDP_segment(self,application_data_payload):
    
    
    
    # define the transmitter function that get application data payload and convert them into UDP segments
    
    # function input parameters: application_data_payload
    # length of application_data_payload is in bytes
    # application data_payload in represented in bytes
    
    
    
    # each segment have the following fields <here we assume UDP packets>
    ###### packet header contains
    
    # pktno: packet number : 4bytes: 32 bits 
    # source_port: this field identifies the sender's port : 2 bytes: 16 bits
    # destination_port: This field identifies the receiver's port: 2 bytes : 16 bits
    # Length: the length in bytes of the UDP header and UDP data : 2 bytes : 16 bits
    # Checksum: the checksum field is used for error-checking of the header and data. 2 bytes : 16 bits 
    # reference byte

    ######

    
    # generates apporperiate number of segments for each application payload
    # length of each segment should be MSS (excluding UDP header)
    
    
    # define pktno 32 bits = 4 bytes 
    
    # calculate number of segments necessary to convert the payload into segments
    number_of_segments = int(math.ceil(len(application_data_payload)/((self.MSS)*1.0)))
   
    
    
    # Generate UDP segments:  each segments should contain MSS bytes of application payload + 12 bytes of UDP  header (pktno + source_port + destination_port + length + checksum)
    
    for segment_no in range(number_of_segments):
      UDP_segment = str()
      head = segment_no * self.MSS
      tail = (segment_no+1) * self.MSS if ((segment_no+1) * self.MSS) < len(application_data_payload) else len(application_data_payload)
      
      
      
      # session_ID : 4 bytes
      UDP_segment += pack('I',self.session_ID)
      
       # segment_no: 4 bytes
      UDP_segment += pack('I',self.current_segment_no)
      
      # source_port: 4 bytes
      UDP_segment += self.source_port
      
      
      # destination_port: 4 bytes
      UDP_segment += self.destination_port
      
      
      
      # reference byte : 1 byte
      if segment_no == 0:
	UDP_segment += pack('B',1)
      elif segment_no == number_of_segments -1:
	UDP_segment += pack('B',2)
      else:
	UDP_segment += pack('B',0)
	
       
      # length: 4 bytes
      length = tail - head 
      UDP_segment += pack('I',length)
     
     
      
      
      # app_payload: MSS bytes
      UDP_segment += application_data_payload[head:tail]
      
      #sys.stderr.write(str(len(application_data_payload[head:tail])) + ',')
      
      # pad zeros to get all segments the same size
      if tail - head < self.MSS:
	zero_byte = pack('B',0)
	UDP_segment += zero_byte * (self.MSS - (tail - head))
	
      
      # CRC: 16 bytes
      m = md5.new()
      m.update(UDP_segment)
      crc = m.digest()
      UDP_segment += crc
      
      
      
      self.current_segment_no +=1
      self.to_network_layer.put(UDP_segment)
      
      
  def transmitter(self):
    
    counter = 0
    while True:
      if not self.from_application_layer.empty():
	app_payload = self.from_application_layer.get()
	self.make_UDP_segment(app_payload)
      else:
	time.sleep(thread_sleep_period)
	counter +=thread_sleep_period
	### debug
	if debug_flag_TNSP_TX and counter % debug_refresh:
	  print "session_ID is: ", self.session_ID
	  print "Length of self.from_application_layer is: ", self.from_application_layer.qsize()
	  print "Length of self.to_network_layer is: ", self.to_network_layer.qsize() 
	 
	
	
	
  
  def decapsulate_segment(self,tnsp_segment):
    
    
    
    segment_no = unpack('I',tnsp_segment[self.field_pos['segment_no'][0]:self.field_pos['segment_no'][1]])[0]
    source_port = unpack('I',tnsp_segment[self.field_pos['source_port'][0]:self.field_pos['source_port'][1]])[0]
    destination_port = unpack('I',tnsp_segment[self.field_pos['destination_port'][0]:self.field_pos['destination_port'][1]])[0]
    reference_byte = unpack('B',tnsp_segment[self.field_pos['reference_byte'][0]:self.field_pos['reference_byte'][1]])[0]
    
    length = unpack('I',tnsp_segment[self.field_pos['length'][0]:self.field_pos['length'][1]])[0]
    app_payload = tnsp_segment[self.field_pos['app_payload'][0]:self.field_pos['app_payload'][0] + length]
    
    crc = tnsp_segment[self.field_pos['crc'][0]:self.field_pos['crc'][1]]
    
    received_segment_md5 = md5.new()
    received_segment_md5.update(tnsp_segment[:self.field_pos['crc'][0]])
    received_segment_crc = received_segment_md5.digest()
    
    if received_segment_crc == crc:
      #sys.stderr.write(str(length) + ',')
      self.payload_recovery_buffer[segment_no] = (reference_byte,app_payload)
      
    
  
  
  
  def get_app_payload(self):
    
    
    head = 0
    tmp_seq = list()
    tmp_payload = str()
    head = 0
    payload_is_complete = False
    for segment_no in self.payload_recovery_buffer:
      #sys.stderr.write(str(segment_no) + ',')
      
      (reference_byte,app_payload) = self.payload_recovery_buffer[segment_no]
      #sys.stderr.write(str(len(app_payload)) + ',')
      if reference_byte == 1:
	payload_is_complete = False
	del tmp_seq[:]
	tmp_payload = ''
      elif reference_byte == 2:
	#sys.stderr.write(str(segment_no) + ',')
	payload_is_complete = True
      
      tmp_payload += app_payload
      tmp_seq.append(segment_no)
        
	
      
      
    
    if payload_is_complete == False:
      return (False,'')
    else:
      for segment_no in tmp_seq:
	#sys.stderr.write(str(segment_no) + ',')
	#sys.stderr.write(str(len(tmp_payload)) + ',')
	del self.payload_recovery_buffer[segment_no]
      return (True, tmp_payload)
      
	
      
    
    
    
    
    
    
  
  def receiver(self):
    
    counter = 0
    
    while True:
      
      if not self.from_network_layer.empty():
	#sys.stderr.write(str(self.to_application_layer.qsize()))
	tnsp_segment = self.from_network_layer.get()
	self.decapsulate_segment(tnsp_segment)
	#sys.stderr.write(str(len(self.payload_recovery_buffer)))
	(suc,app_payload) = self.get_app_payload()
	if suc:
	  #sys.stderr.write("SUC")
	  self.to_application_layer.put(app_payload)
	  
	 
	
	
      else:
	time.sleep(thread_sleep_period)
	counter +=thread_sleep_period
	### debug
	if debug_flag_TNSP_RX and counter % debug_refresh:
	  print "session_ID is: ", self.session_ID
	  print "Length of self.from_network_layer is: ", self.from_network_layer.qsize()
	  print "Length of self.to_application_layer is: ", self.to_application_layer.qsize() 
	 
	
	
    
  
  
  def run(self):
    threading.Thread(target=self.transmitter).start()
    threading.Thread(target=self.receiver).start()
    
    
    
    
    
    
    
    