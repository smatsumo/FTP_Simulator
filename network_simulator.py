import sys
sys.path.insert(0, '/home/iai/Downloads/network_simulator/v1_FTP/DEVICE')
sys.path.insert(0, '/home/iai/Downloads/network_simulator/v1_FTP/APP')
sys.path.insert(0, '/home/iai/Downloads/network_simulator/v1_FTP/TRANSPORT')
sys.path.insert(0, '/home/iai/Downloads/network_simulator/v1_FTP/NET')
sys.path.insert(0, '/home/iai/Downloads/network_simulator/v1_FTP/LL')
sys.path.insert(0, '/home/iai/Downloads/network_simulator/v1_FTP/PHY')
sys.path.insert(0, '/home/iai/Downloads/network_simulator/v1_FTP/GLOBAL')

import node
from global_var import *




#####
## FORMAT GUIDE
## 

class simulator:
  def __init__(self):
    
    node_options = dict()
    self.nodes = dict()
    node_ID = 1
    
    
    for node_ID in range(1,3):
      node_options[node_ID] = dict()
      node_options[node_ID]['sessions'] = dict()
      node_options[node_ID]['sessions']['APP'] = list() 
      node_options[node_ID]['sessions']['TNSP'] = list()
      node_options[node_ID]['NET'] = list()
      node_options[node_ID]['LL'] = list()
      node_options[node_ID]['PHY'] = list()
      node_options[node_ID]['IFCONFIG'] = list()
      
      
    node_ID = 1
    
    node_options[node_ID]['sessions']['APP'].append(('FTP',('FTP_TX.txt','TX')))
    node_options[node_ID]['sessions']['TNSP'].append(('UDP',(50,20000,20001)))
    node_options[node_ID]['sessions']['APP'].append(('FTP',('FTP_TX_2.txt','TX')))
    node_options[node_ID]['sessions']['TNSP'].append(('UDP',(10,20000,20001)))
    node_options[node_ID]['NET'].append(('RIP',('no_options')))
    node_options[node_ID]['LL'].append(('Ethernet',(0))) # 0 in the interface_ID for the LL
    node_options[node_ID]['PHY'].append(('socket_phy',(0,'127.0.0.1','00:21:cc:64:7f:15',12000,12001)))
    node_options[node_ID]['IFCONFIG'].append(('192.168.30.1','00:21:cc:64:7f:15'))
    
    
    self.nodes[node_ID] = node.end_user(node_ID,node_options[node_ID])
    self.nodes[node_ID].run()
    
    
    node_ID = 2
    
    
    node_options[node_ID]['sessions']['APP'].append(('FTP',('FTP_RX.txt','RX')))
    node_options[node_ID]['sessions']['TNSP'].append(('UDP',(50,20000,20001)))
    node_options[node_ID]['sessions']['APP'].append(('FTP',('FTP_RX_2.txt','RX')))
    node_options[node_ID]['sessions']['TNSP'].append(('UDP',(10,20000,20001)))
    node_options[node_ID]['NET'].append(('RIP',('no_options')))
    node_options[node_ID]['LL'].append(('Ethernet',(0))) # 0 in the interface_ID for the LL
    node_options[node_ID]['PHY'].append(('socket_phy',(0,'127.0.0.1','00:21:cc:64:7f:15',12001,12000)))
    node_options[node_ID]['IFCONFIG'].append(('192.168.30.1','00:21:cc:64:7f:15'))
   
    self.nodes[node_ID] = node.end_user(node_ID,node_options[node_ID])
    self.nodes[node_ID].run()
    
   
  
    
    

    
ns = simulator()
