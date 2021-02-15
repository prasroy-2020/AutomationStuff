#!/usr/bin/env python

'''
 Script name: testingtee.py

 Functionality:A sample script to demonstrate the usage of the Tee utility class 
 Usage: python testingtee.py
 Example: python testingtee.py
'''

import os
import sys
#Import the Tee class
from teeutlity import Tee
import traceback

if __name__=='__main__':
    try:
        script_name=os.path.basename(__file__)
        print script_name
        logfile=os.path.abspath(script_name+'.log')
        if os.path.exists(logfile):
            open(logfile, "w").close()
        #redirecting the standard output to Tee class
        sys.stdout = Tee(logfile)
        print "Testing the Tee -a class"
        print "Completed"
        #After the above statement,output will come on the console as well as the logfile
        #reverting the standard output to default
        sys.stdout = sys.__stdout__
    except:
            print "An error has occured "
            print "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
