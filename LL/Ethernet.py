


class Ethernet:
  def __init__(self,interface_MAC_address):
    
    self.current_Ethernet_frame_no = 0
    self.interface_MAC_address = interface_MAC_address
  
  def make_frame(self, net_datagram):
    ### LL Encapsulation
    ### Under Construction
    ## PHY Encapsulation
    self.current_Ethernet_frame_no +=1
    return net_datagram
    
  def get_datagram(self, ll_frame):
    ### LL Decapsulation
     ### Under Construction

	### LL Decapsulation
    return ll_frame
 
  
    