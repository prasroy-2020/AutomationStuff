
import os
import traceback
import xml.etree.ElementTree as ET
import sys
import re
'''
  A basic xml parser for filtering xml documents based on tag values and range of values of a specific 
  tag
'''

class Custom_XmlPar(object):
    def __init__(self, filename):
        self.filename = filename
        
    def Precheck(self, tag_name):
        '''
           Validating whether user has provided a legitimate tag
        '''
        # get an iterable
        context = ET.iterparse(self.filename, events=("start", "end"))
        #List to store all the valid tags
        valid_tags = []
        ##covert into iterator
        doc = iter(context)
        #Fetch the list of valid tags which can be used as filter
        for event, elem in doc:
            if event == "end" and elem.tag == "CD":
                elem.clear()
                break
            elif event == "end" and elem.tag != "CATALOG":
                if elem.tag not in valid_tags:
                    valid_tags.append(elem.tag)
            elem.clear()
        #Validate the user input tag
        if tag_name.upper() not in valid_tags:
            print ("Invalid tag.")
            print ("Following are the valid tags")
            print (valid_tags)
            sys.exit() 
    def filter_by_tag(self, param1, param2):
        '''
            This function will filter xml documents based on the user input (choice == "1")
            and also display matching xml documents based on the price range provided by the user
            (choice == "2")
        '''
        path = []
        # get an iterable
        context = ET.iterparse(self.filename, events=("start", "end"))
        ##covert into iterator
        doc = iter(context)
        event, root = doc.next()
        if isinstance(param2, str):
            pattern = re.compile(param2.upper()) 
        childnode = root.getchildren()
        for element in childnode:
                v_out = ''
                for elem in element.getchildren():
                    v_out += '%s = %s\n' %(elem.tag, elem.text)
                    '''
                    Although iterparse does not consume the entire file at first, 
                    it does not free the references to nodes from each iteration. 
                    When the whole document will be accessed repeatedly, this is a feature. 
                    However, in this case I will reclaim reclaim that memory at the end of each loop. This includes both references to children or text nodes that were already been processed and preceding siblings of the current node, whose references from the root node are also implicitly preserved
                    '''
                    if choice == '1':
                        if elem.tag.upper() == param1.upper() and re.search(pattern, elem.text.upper()) is None:
                           v_out = ''
                           elem.clear()
                           break
                    elif choice == '2':
                        if elem.tag.upper() == 'PRICE':
                            '''
                               Excluding those elements whose price tags are not within the range
                            '''
                            if int(float(elem.text)) < int(float(param1)) or int(float(elem.text)) > int(float(param2)):
                                v_out = ''
                                elem.clear()
                                break
                    elem.clear()
                if v_out:
                       print (v_out)
        root.clear()
                
     
                
if __name__=='__main__':
    try:
        while True:
          print("#"*20)
          print("Menu")
          print("#"*20)
          print("Press 1 for filter by TagName")
          print("Press 2 for filter by price range")
          print ("(Q)uit")
          print("#"*20)
          choice = raw_input(">>> ").lower().rstrip()
          if choice == "q":
             break
          elif choice == "1":
            obj_Custom_XmlPar = Custom_XmlPar('book.xml')
            print ("Enter TagName")
            f_tagname = raw_input(">>> ").lower().rstrip()
            obj_Custom_XmlPar.Precheck(f_tagname)
            print ("Enter Tag Values")
            f_tagval = raw_input(">>> ").lower().rstrip()
            obj_Custom_XmlPar.filter_by_tag(f_tagname, f_tagval)
          elif choice == "2":
              obj_Custom_XmlPar = Custom_XmlPar('book.xml')
              print("Enter Maximum Price")
              try:
                  f_max_price = int(float(raw_input(">>> ").rstrip()))
              except ValueError:
                  print ("Maximum Price cannot be blank.Going back to main menu")
                  continue
              print("Enter Minimum Price")
              try:
                  f_min_price = int(float(raw_input(">>> ").rstrip()))
              except ValueError:
                  print ("Minimum Price cannot be blank.Going back to Main Menu")
                  continue
              if int(float(f_max_price)) < int(float(f_min_price)):
                  print ("Maximum Value %s cannot be less than Minimum Value %s .Going back to Main Menu" %(f_max_price,f_min_price) )
              obj_Custom_XmlPar.filter_by_tag(f_min_price, f_max_price)
          else:
            print("Invalid choice, please choose again\n")
        
    except Exception as e:
        print ("An Error has occured.")
        print ("".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])))
