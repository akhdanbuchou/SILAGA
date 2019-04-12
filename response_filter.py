import mysql_rest as mysql
import re

class Filter:

    def __new__(cls, response, class_filter):
        return class_filter.filter_response(response)

def is_contain_keywords(content, keywords_exclusion):
    for keyword in keywords_exclusion:
        if re.search(r"\b"+re.escape(keyword['keyword'])+r"\b", content.lower()):
            return True
    return False

class OmedClassifiedFilter(object):
    def filter_response(self, responses):

        keywords_exclusion = mysql.retrieve_exclusion_keywords()
        filtered_response = list()
        a = 0
        for response in responses:    
            if not is_contain_keywords(response['content'][0], keywords_exclusion):
                filtered_response.append(response)
        
        return filtered_response

class TelegramFilter(object):

   def filter_response(self, responses):

        keywords_exclusion = mysql.retrieve_exclusion_keywords()
        filtered_response = list()
        
        for response in responses:    
            if not is_contain_keywords(response['laporan'][0], keywords_exclusion):
                filtered_response.append(response)
        
        return filtered_response
        
