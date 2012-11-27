# -*- coding: utf-8 -*-
import urllib2
from xml.dom.minidom import parse, parseString
from types import *

"""
author: akaz
email: yubs87@gmail.com

simple wrapping module used to retrieve postal code from EPOST open api
http://biz.epost.go.kr/eportal/custom/custom_10.jsp?subGubun=sub_4&subGubun_1=cum_20
"""

class EPost():
    def __init__(self, api_key):
        self.api_key = api_key
    def get_postal_code(self, search_keyword):
        """

        retrive all addresses and postal code list via api

        simple usage

        >> ep = EPost("your_api_key_here")

        >> ep.get_postal_code("구의1동")
        >> ep.get_postal_code("논현1동")
 
        """
        if type(search_keyword) is StringType:
            search_keyword = unicode(search_keyword, 'utf-8')

        prefix_url = "http://biz.epost.go.kr/KpostPortal/openapied?regkey={0}&target=post&query=".format(self.api_key)
        req = urllib2.Request(prefix_url + search_keyword.encode('euc-kr'), headers={'Accept-Language': 'ko'})
        content = urllib2.urlopen(req).read()
        
        xml_string = unicode(content, 'euc-kr').encode('utf-8') \
                    .replace('euc-kr', 'utf-8')

        dom = parseString(xml_string) 
        
        if dom.getElementsByTagName('error'):
            error_code = dom.getElementsByTagName('error_code')[0].childNodes[0].nodeValue
            reason = dom.getElementsByTagName('message')[0].childNodes[0].nodeValue
            raise Exception(error_code, reason)
            
        item_list = dom.childNodes[0].childNodes[1]
        addresses = item_list.getElementsByTagName('address')
        postcds = item_list.getElementsByTagName('postcd')
        
        ret = []
        for i, address in enumerate(addresses):
            addr = address.childNodes[0].nodeValue
            postcd = postcds[i].childNodes[0].nodeValue
            ret.append({'address': addr, 'postcd': postcd})

        return ret
