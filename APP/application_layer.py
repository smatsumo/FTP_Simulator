

import FTP
import threading
from global_var import debug_flag_APP

class application_layer:
  def __init__(self,APP_options):
    
    self.APP_options = APP_options
    self.sessions = list()
    
    if debug_flag_APP:
      print self.APP_options
      
    session_ID = 1
    for (protocol,options) in self.APP_options:
      if protocol == 'FTP':
	(FTP_filename,mode) = options
	self.sessions.append(FTP.FTP(session_ID,FTP_filename,mode))
      session_ID +=1
	
  def run(self):
    for session in self.sessions:
      session.run()
    
  