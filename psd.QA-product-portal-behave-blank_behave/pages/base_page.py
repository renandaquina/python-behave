from datasource.datapool import DATA_ACCESS
from datasource.messages import MESSAGES
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from nose.tools import assert_equals
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM
import random
import string
import json
#import pymysql

#----------------------------------------------------------------------------------------------------------------------#
#Import pdb allowed to use the debbuger module using the command line pdb.set_trace(), before the code that you want to#
#analise.                                                                                                              #
#   Example:                                                                                                           #
#           def method_x(args, value):                                                                                 #
#               pdb.set_trace()                                                                                        #
#               while True:                                                                                            #
#                    key = args.popitem(value)                                                                         #
#----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#
# BasePage is a common class where the developer can write the necessary methods in python and re-use on               #
# entire test, make sure the methods that you will write here are flexible, without constants or hardcode              #
# data.                                                                                                                #
# Verify method names are readable to facilitate future maintenance and make it easier for other                       #
# developers to use the method.                                                                                        #
#----------------------------------------------------------------------------------------------------------------------#

class BasePage(object):

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self._timeout = 40
        self.implicit_wait = 40


#----------------------------------------------------------------------------------------------------------------------#
#                     Methods that manipulate strings information as described                                         #
#----------------------------------------------------------------------------------------------------------------------#

####-------------------------------------------- Random Strings Methods --------------------------------------------####

    def generate_unique_id(self, chars_number):
        """Generate N chars random string with Lowercase and Uppercase. """
        """param: integer chars_number"""
        unique_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(chars_number)])
        return unique_id


    def generate_unique_lowercase_id(self, chars_number):
        """Generate N chars random string with Lowercase."""
        """param: integer chars_number"""
        unique_id = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(chars_number)])
        return unique_id


    def generate_unique_uppercase_id(self, chars_number):
        """Generate N chars random string with Uppercase. """
        """param: integer chars_number"""
        unique_id = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(chars_number)])
        return unique_id


    def generate_unique_email(self, username, id, domain_list):
         """Generate random email, combine generate_unique_id,  generate_unique_lowercase_id or generate_unique_uppercase_id
         and a list of domains."""
         """param: string username, string id, list of strings domain_list"""
         """ return string email. Example: anna.01google"""
         email = username +'.'+ id + random.choice(domain_list)
         return email


####----------------------------------------- String Manipulation Methods ------------------------------------------####


    
#----------------------------------------------------------------------------------------------------------------------#
# REPLACE_SPACE is a method designed to replace space froms strings to a underline                                     #                                                                                                                                                                                 
#                                                                                                                      #
# It is necessary to pass the string by parameter                                                                      #                                                                                                                                                                                 
#----------------------------------------------------------------------------------------------------------------------#   
    def replace_space(data):
        return data.replace(' ', '_')


    def split_string_between(self, string_value, slice_a, slice_b):
        """Find and validate before-part and return middle part."""
        pos_a = string_value.find(slice_a)
        if pos_a == -1: return ""
        #Find and validate after part.
        pos_b = string_value.rfind(slice_b)
        if pos_b == -1: return ""
        #Return middle part.
        adjusted_pos_a = pos_a + len(slice_a)
        if adjusted_pos_a >= pos_b: return ""
        return string_value[adjusted_pos_a:pos_b]


    def split_string_before(self, string_value, slice_a):
        """Find first part and return slice before it."""
        pos_a = string_value.find(slice_a)
        if pos_a == -1: return ""
        return string_value[0:pos_a]


    def split_string_after(self, string_value, slice_a):
        """Find and validate first part and returns chars after the found string."""
        pos_a = string_value.rfind(slice_a)
        if pos_a == -1: return ""
        #Returns chars after the found string.
        adjusted_pos_a = pos_a + len(slice_a)
        if adjusted_pos_a >= len(string_value): return ""
        return string_value[adjusted_pos_a:]


    def remove_chars_from_string(self, string_value, char_list):
        """Remove all characters in list from string."""
        new_string = string_value
        for char in char_list:
        #Remove the char in list from the string value.
            new_string = new_string.replace(char, "")
        return new_string


#----------------------------------------------------------------------------------------------------------------------#
#                     Methods that connect and manipulate datasource or database information                           #
#----------------------------------------------------------------------------------------------------------------------#

####-------------------------------------------- Database Methods --------------------------------------------------####

    '''def open_connection_with_database(self, host, port, username, password, database):
        try:
            db_con = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        except Exception:
            print("Error in MySQL connection with "+database+" database.")
        else:
            return db_con'''


    def get_columns_from_dict(self, source, args_key):
        """Convert a dict of arguments into a string to columns separate by comma. Example: 'column_1, column_2, column_3'."""
        str_columns = ""
        data_args = source.get(args_key.replace(' ', '_'))
        if data_args is not None:
            for key, value in enumerate(data_args[0]):
                    str_columns += value + ', '
        else:
                message = "No matching results for parameter data = "+ args_key +" was found in DataPool."
                raise Exception(message)
        return str_columns[:-2]


    def execute_query(self, db_connection, sql_query):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result


    def execute_query_from_db(self, host, port, username, password, database, sql_query):
        connection = BasePage.open_connection_with_database(self, host, port, username, password, database)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result


    def select_all_from_table(self, db_connection, table):
        con = db_connection
        sql_query = "SELECT * FROM " + table
        con.execute(sql_query)
        return con.fetchall()


    def close_connection_database(self, db_connection):
        con = db_connection
        con.close()


#----------------------------------------------------------------------------------------------------------------------#
# DATAPOOL_READ is a method use to get a collection of information from a source archive Dictionaries, Hashmaps, and   #
# Hash Tables. This method need 3 arguments: the dict's name, the collection's name and the key that you searching for.#
#                                                                                                                      #
#   Example:                                  result = datapool_read(DATA_SOURCE, valid_data, 'key_1')                 #
#       DATA_SOURCE ={                        print("Results is: ", result)                                            #
# 	        "valid_data" :[{                                                                                           #
# 	                 "key_1" : "value1",                                                                               #
#      	             "key_2" : "value2"       output:  Results is: value1                                              #
#      	     }],                                                                                                       #
#           "invalid_data" :[{                                                                                         #
# 	                "key_1" : "value1",                                                                                #
#      	            "key_2" : "value2"                                                                                 #
#      	            }]                                                                                                 #
# }                                                                                                                    #                                                                          #
#----------------------------------------------------------------------------------------------------------------------#
    def datapool_read(self, source, data, key):
        """Get a list of arguments named as 'data' on the 'source' and search the 'key' on that list."""
        data_args = source.get(self.replace_space(data))
        dt_key = self.replace_space(key)
        #key.replace(' ', '_')
        if data_args is not None:
            #Search the 'key' on that list
            if data_args[0].get(dt_key)is not None:
                return data_args[0].get(dt_key)
            else:
                message = "No matching results for parameter data = "+ data +" on the key = " + key +" was found in DataPool."
                raise Exception(message)
        else:
            message = "No matching results for parameter data = "+ data +" on the key = " + key +" was found in DataPool."
            raise Exception(message)

#----------------------------------------------------------------------------------------------------------------------#
# GET_LIST_FROM_SOURCE is a method use to load a data from a source archive. It's useful to get all information        #
# from a collection. For example, if you need to POST the same .json and the data don't need to be changed, the data   #
# source can emulate the .json.                                                                                        #
# This method need 2 arguments: the dict's name and the collection's name:                                             #
#   Example:                                                                                                           #
#       DATA_SOURCE ={                     payload = get_list_from_source(DATA_SOURCE, 'valid_data')                   #
# 	        "valid_data" :[{               print("Payload is: ", payload)                                              #
# 	                 "key_1" : "value1",                                                                               #
#      	             "key_2" : "value2"                                                                                #
#      	     }],                           output:  Payload is:   "valid_data" :[{                                     #
#           "invalid_data" :[{                                           "key_1" : "value1",                           #
# 	                "key_1" : "value1",                                  "key_2" : "value2"                            #
#      	            "key_2" : "value2"                                   }]                                            #
#      	            }]                                                                                                 #
# }                                                                                                                    #                                                                          #
#----------------------------------------------------------------------------------------------------------------------#

    def get_list_from_source(self, source, data):
        """Get a list of arguments named as 'data' on the 'source'."""
        data_args = source.get(data.replace(' ', '_'))
        if data_args is not None:
            #Return the list if not Empty
            return data_args[0]
        else:
            message = "No matching results for parameter data = "+ data +" was found in DataPool."
            raise Exception(message)


    def get_data_from_dict(self, dict_args , key):
        """Get a dictionary of arguments named as 'dict_args', search the 'key' on that dict and return the value."""
        data_args = dict_args
        if data_args is not None:
            #Search the 'key' on that list
            if data_args.get(key)is not None:
                return data_args.get(key)
        else:
            message = "No matching results for parameter key = "+ key +" was found in Dictionary."
            raise Exception(message)


#----------------------------------------------------------------------------------------------------------------------#
#                                 Methods exclusive for UI testing tool                                                #
#----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#
# COMPARE_URL is a method designed to verify if expected url is the same as current url                                #                                                                                                                                                                                 
#                                                                                                                      #
# It is necessary to pass both urls by parameter                                                                   #                                                                                                                                                                                 
#----------------------------------------------------------------------------------------------------------------------#
    def compare_url(context, expected_url, current_url):
        try:
            WebDriverWait(context.browser, 60).until(EC.url_to_be(expected_url))
        except TimeoutException:
            message = "Some error occurred and the expected page did not load.\n\nExpected url: " + expected_url + "\nCurrent url: " + current_url
            raise Exception(message)

#----------------------------------------------------------------------------------------------------------------------#
# COMPARE_MESSAGE is a method designed to verify if expected message is the same as result message       #                                                                                                                                                                                 
#                                                                                                                      #
# It is necessary to pass both messages by parameter                                                                   #                                                                                                                                                                                 
#----------------------------------------------------------------------------------------------------------------------#
    def compare_message(expected_message, current_message):
        try:
            assert_equals(expected_message, current_message)
        except AssertionError:
            message = "The expected message/title was different than the current message/title.\n\nExpected message/title: " + expected_message + "\nCurrent message/title: " + current_message
            raise Exception(message)

#----------------------------------------------------------------------------------------------------------------------#
# ELEMENT_DISPLAYED is a method designed to verify if some element is displayed (visible)                              #                                                                                                                                                                                 
#                                                                                                                      #
# It is necessary to pass the locator of which element will be analyzed by parameter                                   #                                                                                                                                                                                 
#----------------------------------------------------------------------------------------------------------------------#
    def element_displayed(self, context, locator):
        try:
            WebDriverWait(context.browser, 60).until(EC.visibility_of_element_located((locator.l_type, locator.selector)))
        except TimeoutException:
            message = "The element or the selector "+ locator.selector +" is not visible, can't be found or it doesn't exist on the screen."
            raise Exception(message)
        return True
    
#----------------------------------------------------------------------------------------------------------------------#
# ELEMENT_EXISTS is a method designed to if some element exists on page with Webdriverwait                             #
#                                                                                                                      #
# It is necessary to pass the locator of which element will be analyzed by parameter                                   #                                                                                                                                                                                 
#----------------------------------------------------------------------------------------------------------------------#
    def element_exists(self, context, locator, time):
        try:
            WebDriverWait(context.browser, time).until(EC.presence_of_element_located((locator.l_type, locator.selector)))
        except TimeoutException or NoSuchElementException:
            message = "The page did not load, the element or the selector "+ locator.selector +" can't be found or it doesn't exist on the screen."
            raise Exception(message)
        return True


#----------------------------------------------------------------------------------------------------------------------#
# ELEMENT_IS_VISIBLE is a method designed to verify if some element is visible                                         #
#                                                                                                                      #
# It is necessary to pass the locator of which element will be analyzed by parameter                                   #                                                                                                                                                                                 
#----------------------------------------------------------------------------------------------------------------------#
    def element_is_invisible(self, context, locator, time):
        try:
            WebDriverWait(context.browser, time).until(EC.invisibility_of_element_located((locator.l_type, locator.selector)))
        except TimeoutException or NoSuchElementException:
            return False
        return True

#----------------------------------------------------------------------------------------------------------------------#
# GET_ELEMENT is a method designed to find and get the current element                                                 #                                                                                                                                                                                 
#                                                                                                                      #
# It is necessary to pass the locator of which element will be analyzed by parameter                                   #
#----------------------------------------------------------------------------------------------------------------------#
    def get_element(self, context, locator):
        if not self.locate_element(self, context, locator):
            raise NoSuchElementException("Could not find {locator.selector}")
        return context.browser.find_element(locator.l_type, locator.selector)


#----------------------------------------------------------------------------------------------------------------------#
# LOCATE_ELEMENT is a method designed to locate an element on page                                                        #                                                                                                                                                                                 
#                                                                                                                      #
# It is necessary to pass the locator of which element will be analyzed by parameter                                   #
#----------------------------------------------------------------------------------------------------------------------#
    def locate_element(self, context, locator):
        try:
            return WebDriverWait(context.browser, 140).until(EC.presence_of_element_located((locator.l_type, locator.selector)))
        except TimeoutException:
             message = "The element or the selector "+ locator.selector +" can't be found or it doesn't exist on the screen."
             raise Exception(message)


#----------------------------------------------------------------------------------------------------------------------#
# ELEMENT_IS_CLICKABLE is a method designed to verify if an element is clickable                                       #                                                                                                                                                                                 
#                                                                                                                      #
# It is necessary to pass the locator of which element will be analyzed by parameter                                   #
#----------------------------------------------------------------------------------------------------------------------#
    def element_is_clickable(self, context, locator):
        try:
            return WebDriverWait(context.browser, 20).until(EC.element_to_be_clickable((locator.l_type, locator.selector)))
        except TimeoutException:
             message = "The element or the selector "+ locator.selector +" is not clickable or it doesn't exist on the screen."
             raise Exception(message)

    
#----------------------------------------------------------------------------------------------------------------------#
# LOCATE_ELEMENT_SCREEN is a method designed to is a method designed to locate an element on page                      #                                                                                                                                                                                 
#                                                                                                                      #
# It is necessary to pass the locator of which element will be analyzed by parameter                                   #
#                                                                                                                      #                        
# This method was created specially for layout validation feature                                                      #
#----------------------------------------------------------------------------------------------------------------------#
    def locate_element_screen(self, context, locator, element):
        try:
            if "menu" in element:
                WebDriverWait(context.browser, 20).until(EC.presence_of_element_located((locator.l_type, locator.selector))).click()
            elif "options" in element:
                WebDriverWait(context.browser, 20).until(EC.presence_of_element_located((locator.l_type, locator.selector))).click()
            else:
                WebDriverWait(context.browser, 20).until(EC.presence_of_element_located((locator.l_type, locator.selector)))
        except TimeoutException:
             message = "The element or the selector "+ element +" can't be found or it doesn't exist on the screen."
             raise Exception(message)

#------------------------------------------------------------------------------------------------------------------------------#
# SOME_MESSAGE_SHOULD_APPEAR is a method designed to check if some error/message appeared during the test, in this case if a   #
# error/message was not thrown the the test failed                                                                             #
#                                                                                                                              #
# It is necessary to pass the locator of which input will be analyzed by parameter and which error/message should appear.      #
#------------------------------------------------------------------------------------------------------------------------------#
    def some_message_should_appear(context, page, message_key, messageInput):
        base_page = BasePage
        # Getting the attribute (location of element) from class, passing the current input as parameter
        current_input = getattr(page, BasePage.replace_space(messageInput)) 
        element_isDisplayed = BasePage.element_displayed(base_page, context, current_input)
        # If no message appears on the current input then the exception is thrown
        if not element_isDisplayed:
            raise Exception("The element was not found or the message not appeared on the " + messageInput + " field")
        else:
            current_message = BasePage.get_element(base_page, context, current_input).text
            expected_message = base_page.datapool_read(base_page, MESSAGES, "message", message_key)
            BasePage.compare_message(expected_message, current_message)


    #testar
    def verify_element_list(self, driver, timeout, element_list):
        """"Given list of element like: LAYOUT_LIST = [{element, type, text_expected}, {element, type, text_expected}],
        this method will verify if the elements on the list is on the screen or if the expected data text is on the screen. 
        If it fails a report is return."""
        fail_results = []
        for key in element_list:
            element = BasePage.get_data_from_dict(self, key, "element")
            type = BasePage.get_data_from_dict(self, key, "type")
            text_expected = BasePage.get_data_from_dict(self, key, "text_expected")
            if text_expected == "":
                 if BasePage.element_exists(self, driver, timeout, type, element) is False:
                     message = "The element "+ element + " can't be found or it doesn't exist on the screen."
                     fail_results.append(message)
                 else:
                     pass
            else:
               if BasePage.element_exists(driver, timeout, type, element) is False:
                     message = "The element "+ element + " can't be found or it doesn't exist on the screen."
                     fail_results.append(message)
               else:
                   text_obtained = BasePage.locate_element(self, driver, timeout, type, element).text
                   if text_obtained == text_expected:
                      pass
                   else:
                      message = "The text shown by the "+ str(element) + " on the screen is different that was expected. It was expected: '"+str(text_expected)+"' and was obtained: '"+str(text_obtained)+"'."
                      fail_results.append(message)
        if fail_results is not None:
            raise Exception(fail_results)



#----------------------------------------------------------------------------------------------------------------------#
#                     Methods manipulate XML files information and responses                                           #
#----------------------------------------------------------------------------------------------------------------------#

####----------------------------------------------- XML Methods ----------------------------------------------------####
#----------------------------------------------------------------------------------------------------------------------#
# READ_XML_FILE is a method use to load a generic .xml archive.                                                        #
# This method need 1 argument: the path of the .xml. It will return the generic.xml allowing to access namespaces      #
# and/or edit them if it's necessary.                                                                                  #
#   Example:                                                                                                           #
#        payload = read_xml_file(os.path.dirname(__file__) + '\\data_source\\generic.xml')                             #	                                                                                               #
#----------------------------------------------------------------------------------------------------------------------#

    def read_xml_file(self, xml_file):
        """Given a XML file, this method open it and return entire XML body."""
        xml = open(xml_file, 'r')
        body = xml.read()
        return body


#----------------------------------------------------------------------------------------------------------------------#
# GET_XML_ROOT is a method use to get the root from a .xml response tree.                                              #
# This method need 1 argument: the response .xml from an API. It will get the content of the response and return the   #
# root.                                                                                                                #
#   Example:                                                                                                           #
#        root_tree = get_xml_root(xml_response)                                                                        #	                                                                                               #
#----------------------------------------------------------------------------------------------------------------------#

    def beautify_xml(self, element):
        """Return a pretty-printed XML string for the Element."""
        element_content = element
        if type(element_content)!= bytes and type(element_content)!= str:
            element_content = element.content.decode("utf-8")
        reparsed = DOM.parseString(element_content)
        return reparsed.toprettyxml(indent="\t")


    def verify_responses_status(self, response, request, xml):
        if str(response) != '<Response [500]>':
            return True
        else:
            message = "The status is "+str(response)+". The system is disable, suspended or the request is badly formatted."
            print("Resquest used: \n", request)
            print("Obtained Response: \n", BasePage.beautify_xml(self, response.content))
            raise Exception(message)


    def get_xml_root(self, response):
        """Given a XML File or XML response from an API, this method open it and return the root(iterable)."""
        response_content = response
        if type(response_content)!= bytes and type(response_content)!= str:
            response_content = response.content.decode("utf-8")
        #Transform the content into tree(iterable)
        response_tree = ET.ElementTree(ET.fromstring(response_content))
        response_root = response_tree.getroot()
        return response_root

    #testar
    def find_value_on_xml(self, response, tag):
        """Given a XML response from API and specific tag name, this method search that tag name and return the value."""
        #Get the root from the XML File or XML response from an API
        response_root = BasePage.get_xml_root(self, response)
        #Search the element where the tag name is
        for element in response_root.iterfind('.//'+ tag):
            #Return the value
            return element.text


    #testar
    def tag_exists_on_xml(self, response, tag):
        """Given a XML response from API and specific tag name, this method search if that tag name exists on the XML response and return a boolean."""
        #Get the root from the XML File or XML response from an API
        response_root = BasePage.get_xml_root(self, response)
        #Search the element where the tag name is
        for element in response_root.iterfind('.//'+ tag):
            return True
        return False


    #testar
    def tag_list_exists_on_xml(self, response, tag_list):
        """Given a XML response from API and specific list of tags, 
        this method verify if all tags exists in the response and return a boolean."""
        args = tag_list
        #Search the list of elements
        for args_key, args_value in args.items():
            item = BasePage.tag_exists_on_xml(self, response, args_value)
            #Validate if tag exists
            if item is True:
                pass
            else:
                return False
        return True


    #testar
    def tag_list_is_on_xml(self, response, tag_list, namespace):
        """Given a XML response from API and specific list of tags, this method verify if all tags are in the response."""
        args = tag_list
        #Search the list of elements
        for key in args.items():
                item = BasePage.tag_exists_on_xml(self, response, key)
                #Validate the tag name when it is found
                if item is True:
                    #print("The tag <"+ key[1].replace(namespace, "")+"> on the tag list was in the XML response.")
                    pass
                else:
                    message = "The tag <"+ key.replace(namespace, "") +"> on the tag list wasn't in the XML response."
                    raise Exception(message)


    #testar
    def verify_hit(self, response, tag_list):
        """Given a XML response from API and specific list of tags, this method verify if all tags are in the response."""
        args = tag_list
        #Search the list of elements
        for key in args.items():
            item = BasePage.tag_exists_on_xml(self, response, key)
            #Validate the value when it is found
            if item:
                return True
            else:
                return False

    #testar
    def confirm_persistence_of_response_in_different_sources(self, source_a, source_b, args, namespace_a, namespace_b, source_name_a, source_name_b):
        """Given an XML File or XML response in different sources, this method search in the both sources the tag names
        and validate the values."""
        fail_list=[]
        for key in args.items():
            #Get tag name from both arguments list
            #Search them in their respective XML File or XML response
            item_a = BasePage.find_value_on_xml(self, source_a, key[1])
            item_b = BasePage.find_value_on_xml(self, source_b, key[1])
            #Validate the value when it is found
            if item_a == item_b:
                #print("The values on the "+ key[1] +" = "+ str(item_a) +" and "+ key[1] + " = "+ str(item_b)+" match.")
                pass
            else:
                message = "The values on the "+source_name_a+" "+ key[1].replace(namespace_a, "") +" = "+ str(item_a) +" and "+source_name_b+" "+ key[1].replace(namespace_b, "") + " = "+ str(item_b)+" didn't match."
                fail_list.append(message)
        if not fail_list:
            pass
        else:
            message ="End of Fail List"
            print(*fail_list, sep="\n")
            raise Exception(message)


    #testar
    def compare_values_from_two_xml(self, xml_a, xml_b, args_a, args_b, namespace_a, namespace_b, source_name_a, source_name_b):
        """Given two XML Files, this method search in the both files the tag name arguments and validate the values."""
        fail_list=[]
        while True:#It simulate a DO/WHILE
            #Pop the first tag name from both arguments list
            key_a = args_a.popitem()
            key_b = args_b.popitem()
            #Search them in their respective XML File or XML response
            item_a = BasePage.find_value_on_xml(self, xml_a, key_a[1])
            item_b = BasePage.find_value_on_xml(self, xml_b, key_b[1])
            #Validate the value when it is found
            if item_a == item_b:
                #print("Match on the "+ key_a[1].replace(namespace_a, "") +" = "+ str(item_a) +" and "+ key_b[1].replace(namespace_b, "") + " = "+ str(item_b)+" match.")
                pass
            else:
                message = "The values on the "+source_name_a+" "+ key_a[1].replace(namespace_a, "") +" = "+ str(item_a) +" and "+source_name_b+" "+ key_b[1].replace(namespace_b, "") + " = "+ str(item_b)+" didn't match."
                #Stored the path list
                fail_list.append(message)
            count_args_a = len(args_a)
            count_args_b = len(args_b)
            #Stop the loop when one of the arguments list end
            if count_args_a <= 0 or count_args_b <= 0:
                break
        if not fail_list:
            pass
        else:
            message ="End of Fail List"
            print(*fail_list, sep="\n")
            raise Exception(message)


    #testar
    def list_all_paths_on_xml_starting_from_node(self, path_list, response_root, start_path,namespace, node_name):
        """Given a XML File or XML response from an API, it will list all path starting it from a specific node. It will
        return the entire path for example 'Body > Parent > Child1' if it start from Body the path will be 'Parent/Child1'"""
        #Start from the root of XML File or XML response from an API
        for element in response_root:
            element_name = ET.QName(element.tag)
            #Get the parent tag name without namespace
            parent = element_name.text.strip().lstrip(namespace)
            #Test if it is a parent or child and concatenate to the new path
            if not element.getchildren() and element.text:
                new_path = start_path + "/" + parent
            else:
                new_path = start_path + "/" + parent
                BasePage.list_all_paths_on_xml_starting_from_node(self, path_list, element, new_path, namespace, node_name)
            #Once the entire path is stored, manipulate the string to get the path that starts only from the desired node.
            path = BasePage.split_string_after(self, new_path, node_name)
            #Clean the Empty path
            if path != "":
                #Stored the path list
                path_list.append(path)
        return path_list


    #testar
    def list_all_full_paths_on_xml(self, path_list, response_root, start_path, namespace):
        """Given a XML File or XML response from an API, it will list all full path from it'"""
        #Start from the root of XML File or XML response from an API
        for element in response_root:
            element_name = ET.QName(element.tag)
             #Get the parent tag name without namespace
            parent = element_name.text.strip().lstrip(namespace)
             #Test if it is a parent or child and concatenate to the new path
            if not element.getchildren() and element.text:
                new_path = start_path + "/" + parent
            else:
                new_path = start_path + "/" + parent
                BasePage.list_all_full_paths_on_xml(self, path_list, element, new_path, namespace)
            #Stored the path list
            path_list.append(new_path)
        return path_list


    #testar
    def compare_pathlist_from_two_xml_responses(self, context, system_name_a, system_name_b, response_a, response_b, namespace_a, namespace_b, node_name_a, node_name_b):
        """Given two XML Files or two XML responses, this method search in the both responses or both files divergent
        paths starting from a specific node and validate it. If any divergent path is found an report of divergences will be provide."""
        #Get both root
        xml_root_a = BasePage.get_xml_root(self, response_a)
        xml_root_b = BasePage.get_xml_root(self, response_b)
        #Define the path lists and result lists before call the method
        list_a = []
        list_b = []
        result_a = []
        result_b = []
        #Get the path list
        path_list_a = BasePage.list_all_paths_on_xml_starting_from_node(self, list_a, xml_root_a,"",namespace_a, node_name_a)
        path_list_b = BasePage.list_all_paths_on_xml_starting_from_node(self, list_b, xml_root_b,"",namespace_b, node_name_b)
        print("\nResponse Count Path "+system_name_a+":",len(list(path_list_a)),"Response Count Path "+system_name_b+":",len(list(path_list_b)))
        #Get the intersection of both path lists, sort it alphabetically and count the result
        divergent_paths = sorted(set(path_list_a).symmetric_difference(set(path_list_b)))
        divergent_count = len(list(divergent_paths))
        #If any divergence is found the report will be shown
        if divergent_count == 0:
           pass
        else:
            print("Total Divergent Paths: ",divergent_count,"Divergent Paths List: ",*divergent_paths, sep="\n")
            for path_a in path_list_a:
                if path_a in path_list_b:
                    pass
                else:
                    result_a.append(path_a)
            count_result_a = len(list(result_a))
            for path_b in path_list_b:
                if path_b in path_list_a:
                    pass
                else:
                    result_b.append(path_b)
            count_result_b = len(list(result_b))
            print("\nTotal Divergent Paths "+system_name_a+":",count_result_a, system_name_a+":", *result_a, sep="\n")
            print("\nTotal Divergent Paths "+system_name_b+":",count_result_b, system_name_b+":", *result_b, sep="\n")
            message =  "End of Divergent Paths Report"
            raise Exception(message)


#----------------------------------------------------------------------------------------------------------------------#
#                     Methods manipulate JSON files information and responses                                          #
#----------------------------------------------------------------------------------------------------------------------#

####----------------------------------------------- JSON Methods ---------------------------------------------------####

    #testar
    def key_exists(self, context, key):
        json_key = BasePage.find_key_on_json(self, context.json, key)
        if json_key == key:
            return True
        else:
            return False


    #testar
    def value_is_correct(self, context, key, value):
        if value == 'null':
            value = None
        if BasePage.key_exists(self, context, key) is True:
            return True
        if context.value == value:
            return True
        else:
            return False


    #testar
    def find_value_json(self, obj, key):
        if key in obj:
            return obj[key]
        if type(obj) is dict:
            for k, v in obj.items():
                if isinstance(v, dict):
                    return BasePage.find_value_json(self, v, key)
        elif type(obj) is list:
            for k, v in enumerate(obj):
                return BasePage.find_value_json(self, v, key)


    #testar
    def find_key_on_json(self, obj, key):
        if key in obj:
            return key
        for k, v in obj.items():
            if isinstance(v, dict):
                item = BasePage.find_key_on_json(self, v, key)
                if item is not None:
                    return item


    #testar
    def find_key_and_replace_value_json(self, obj, key, value):
        if key in obj:
            obj[key]=value
            return obj[key]
        if type(obj) is dict:
            for k, v in obj.items():
                if isinstance(v,dict):
                    item = BasePage.find_key_and_replace_value_json(self, v, key, value)
                    if item is not None:
                        return json.dumps(obj, indent=4, sort_keys=True)
        elif type(obj) is list:
            for k, v in enumerate(obj):
                item = BasePage.find_key_and_replace_value_json(self, v, key, value)
                if item is not None:
                   return json.dumps(obj, indent=4, sort_keys=True)


    #testar
    def edit_json(self, json_file_path, args):
        json_file = json_file_path
        with open(json_file, 'r') as file:
            json_data = json.load(file)
            for args_key, args_value in args.items():
                for key, value in json_data.items():
                    v = json_data[key]
                    if(type(v) is dict)or(type(v) is list):
                        item = BasePage.find_key_and_replace_value_json(self, v, args_key, args_value)
                        if(item is not None)or(type(item) is str):
                           json.dumps(json_data, indent=4, sort_keys=True)
                        for v_key, v_value in v.items():
                            v1 = v[v_key]
                            if(type(v1) is dict)or(type(v1) is list):
                                BasePage.find_key_and_replace_value_json(self, v1, args_key, args_value)
        new_json = json.dumps(json_data, indent=4, sort_keys=True)
        return new_json


