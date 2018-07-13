



class RIP:
  def __init__(self,interface_IP_addresses):
    
    self.current_datagram_no = 0
    self.interface_IP_addresses = interface_IP_addresses
  
  def make_datagram(self, tnsp_segment):
    
    ### NET Encapsulation
    ### Under Construction
    ## NET Encapsulation
    
    self.current_datagram_no +=1
    return tnsp_segment
    
  def get_segment(self, net_datagram):
     ### NET Decapsulation
     ### Under Construction
     ### NET Decapsulation
     return net_datagram
 
  def get_interface_IP_address(self):
    # we will return the right interface_IP_address based on the routing algorithm
    # for now we just return the default value
    
    return self.interface_IP_addresses[0][0]
    

   
    
    
      