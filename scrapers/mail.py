# coding=utf-8

import urllib2, urllib, cookielib, time, getpass
from urllib2 import build_opener, HTTPCookieProcessor
from urllib import urlencode
from cookielib import CookieJar
from time import localtime
from getpass import getpass

class session:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.auth = False
        self.opener = urllib2.build_opener()
        
    def sendsms(self, fromhp='', tohp='', msg=''):
        cj = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cj))
    

        
        # Login session
        loginurl = 'http://mail.kaist.ac.kr/nara/servlet/user.UserServ' 
        
        parameters = {
            'cmd': 'login',
            #'strUri':'',
            'DOMAIN': 'kaist.ac.kr',
            'USERS_ID': self.username,
            'USERS_PASSWD': self.password,
        }
            
        values = urlencode(parameters) # Sets the parameters as the POST data
        
        response = opener.open(loginurl, values) # Retrieves the cookies + logs in the system
        html = response.read()    
        
        time = localtime()
        smsparameters = {
            'formType': 'short',
            'sendHp': fromhp,
            'toMessage': msg,
            'msglen': len(msg),
            'mglenLimit': '/80',
            'quota': '45', # Remaining sms?
            'receivePhone': '',
            'receiveCount1': '1',
            'receiveHp': tohp,
            'sendPhone': fromhp,
            'type':	'0',
            'SMS_REQUEST_SEND_DATE': '',
            'SMS_REQUEST_SEND_DATE_year': time.tm_year,
            'SMS_REQUEST_SEND_DATE_month':	time.tm_mon,
            'SMS_REQUEST_SEND_DATE_date': time.tm_mday,
            'SMS_REQUEST_SEND_DATE_hour': time.tm_hour,
            'SMS_REQUEST_SEND_DATE_minute': time.tm_min,
            'flag_no': 'All'
        }
        
        sms = urlencode(smsparameters)
        
        #REMOVE THE COMMENT FROM NEXT LINE TO ENABLE SMS SENDING
        response = opener.open('http://mail.kaist.ac.kr/nara/servlet/sms.SmsServ?cmd=sms_01_010c', sms)
    
if __name__ == "__main__":
  main()
