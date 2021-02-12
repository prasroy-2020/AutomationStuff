#!/usr/bin/env python
#====================================================================================================================
# Script name: get_datacenter_details.py
#
# Functionality:A sample script to demonstrate endpoint processing without using requests library.The endpoint takes one input podname
#               From the Endpoint output the script is fetching a specific field dbcode value 
# Usage: python get_datacenter_details.py <podname>
# Example: python get_datacenter_details.py xxx
# Created by: Prasanta Kr Roy
#

#====================================================================================================================
import os
import sys
import urllib2
import json
import traceback
import time
from ConfigParser import SafeConfigParser

class allpodinfo():
        def __init__(self,podname):
                
                ''' 
                    Fetching the endpoint and the credentials from the config file 
                '''
                self.podname = podname  
                v_config_ini=os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))
                parser = SafeConfigParser()
                parser.optionxform = str
                parser.read(v_config_ini)
                self.v_url = parser.get('API','endpoint')
                self.v_usr= parser.get('API','username')
                self.v_pwd = parser.get('API','password')
                self.v_derived_url = self.v_url+self.podname+'&request_type=all'  #This line is not needed if the endpoint don't take any arguments
                self.no_of_retry = parser.get('API','num_of_retries')        
                self.time_interval = parser.get('API','time_interval')        
        
        def getdcname(self , podname):
                ''' 
                    This function will invoke the endpoint using the podname parameter provided in the input and parse the json 
                    file for dbcode field.It will also retry accessing the endpoint incase of failures.The number of retries
                    are mentioned in the config.ini file 'num_of_retries'
                '''
                #Creates the password Manager            
                passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                passmgr.add_password(None, self.v_derived_url, self.v_usr, self.v_pwd)
                
                #Create the authentication handler
                bas_auth_handler = urllib2.HTTPBasicAuthHandler(passmgr)
                v_opener = urllib2.build_opener(bas_auth_handler)
                urllib2.install_opener(v_opener)

                for _ in range(int(self.no_of_retry)):

                    try:
                        results = json.loads(pagehandle.read())
                        v_db_code = results.get('dbcode')
                    except Exception:
                        time.sleep(int(self.time_interval))
                        return "Db code not found"
                    return v_db_code
def usage():
        print '''Usage: python get_datacenter_details.py <PODNAME>
        E.g.python  python get_datacenter_details.py XXXXXXX '''
if __name__== '__main__':
        if len(sys.argv)<2:
                print "Podname should be provided"
                usage()
                sys.exit(1)
        try:
            podname = sys.argv[1]
            obj_allpodinfo = allpodinfo(podname)
            data_center = obj_allpodinfo.getdcname(podname)
            if data_center:
                print "Db Code = %s" %(data_center)
            else:
                print "Db Code is blank"
        except:
            print "An error has occured fro podname %s" %(podname)
            print "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))

