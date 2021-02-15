#!/usr/bin/env python
#====================================================================================================================
# Script name: getJsonfield.py
#
# Functionality:A sample script to demonstrate endpoint processing without using requests library.The endpoint takes one input podname.
#               From the Endpoint output the script fetches the value of the specific field provided by the user 
# Usage: python getJsonfield.py <podname>
# Example: python getJsonfield.py xxx
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
        def __init__(self, podname, json_field):
                
                ''' 
                    Fetching the endpoint and the credentials from the config file 
                '''
                self.podname = podname  
		        self.json_field = json_field
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
        
        def getjsonfield(self):
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
			            print "Accessing the following  url: %s" %(self.v_derived_url)
			            pagehandle = urllib2.urlopen(self.v_derived_url)
                        results = json.loads(pagehandle.read())
			            return self.parse_json(results)
                    except Exception:
                        time.sleep(int(self.time_interval))
                        return "None"
        def parse_json(self,jsondata):
		    for key,values in jsondata.items():
    			    if isinstance(values, list):
      				    for elm in values:
                            #If the child is an array iterate through the individual elements
        				    self.parse_json(elm)
    			    elif isinstance(values, dict):
                            #If the child is a dict search through the individual keys
				            for child_key,child_values in values.items():
      					        if self.json_field in child_key:
        					        return child_values
			        else:
				            if self.json_field in key:
        				        return values
def usage():
        print '''Usage: python getJsonfield.py <PODNAME> <Jsonfieldname>
        E.g.python  python getJsonfield.py XXXXXXX XXXX'''
if __name__== '__main__':
        if len(sys.argv)<3:
                print "Podname and json field name should be provided"
                usage()
                sys.exit(1)
        try:
            podname = sys.argv[1]
	        json_field = sys.argv[2]
            obj_allpodinfo = allpodinfo(podname, json_field)
            v_json_field = obj_allpodinfo.getjsonfield()
            if v_json_field:
                print "Json Field %s value = %s" %(json_field,v_json_field)
            else:
                print "Json Field %s is blank" %(json_field)
        except:
            print "An error has occured fro podname %s" %(podname)
            print "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))


