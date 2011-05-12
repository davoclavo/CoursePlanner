# coding=utf-8

#import sys
#sys.path.insert(0, "/Users/David/Dropbox/Python/Django/")

import cookielib, urllib, urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from CoursePlanner.models import *
from django.contrib.auth.models import User

class session:
    # To keep the session, the headers will save the JSESSIONID
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.auth = False
        self.headers = {}
        
    def login(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65 Safari/534.24'),
            ]
        
        home = opener.open('http://kaipa.kaist.ac.kr/')
        sessid = cj._cookies['kaipa.kaist.ac.kr']['/']['JSESSIONID'].value
        self.headers = {
            'Cookie': 'JSESSIONID='+sessid,
            }
        
        #username = raw_input('User: ')
        #import getpass
        #password = getpass.getpass()
        
        # Login session
        url = 'http://kaipa.kaist.ac.kr/login_check_eng.jsp'
        parameters = {'p_id': self.username, 'p_password': self.password}
        values = urllib.urlencode(parameters)
        req = urllib2.Request(url, values, self.headers)
        response = urllib2.urlopen(req)
    
        html = response.read()
        
        if html.find('KAIST Intranet')>0 and html.find('You are not')==-1:
            print '--Authentificated: ' + self.username 
            self.auth = True
        else:
            print '--Wrong user/password'
        return self.auth
            
    def takecourses(self):
        if not self.auth:
            print 'Invalid session'
            pass
            
        url = 'http://kaipa.kaist.ac.kr/sg/sj_sjjh_list_eng.jsp'
        req = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(req)
        rawhtml = response.read()
        
        soup = BeautifulSoup(rawhtml)
        coursestable = soup('tr',{'class' : 'List_2'})
        coursestaken = []
        #print len(coursestable)
        for course in coursestable:
            # Header_9 is for the titles of the each semester, so we remove them from the list
            if course.td['class'] != 'Header_9':
                # All the td tags are the properties of the course
                coursestaken.append(course.findAll('td'))
        number = 0
        user, dummy = User.objects.get_or_create(username=self.username)
        self.deletealltaken(user)
        for coursetaken in coursestaken:
            number += 1
            dept = getcleantext(coursetaken[1].text)
            code = getcleantext(coursetaken[2].text)
            #section = getcleantext(coursetaken[3].text)
            classification = getcleantext(coursetaken[4].text)
            title = getcleantext(coursetaken[5].text)
            #code = ':)'
            grade = getcleantext(coursetaken[11].text)
            koreanname = getcleantext(coursetaken[12].text)
            #print "'%s', '%s' , '%s' , '%s' , '%s' , '%s' , '%s'" % (number, dept, code, classification, title, grade, koreanname)
            
            
            course = TakenCourse(
                number=number,
                dept=dept,
                code=code,
                classification=classification,
                title=title,
                grade=grade,
                koreanname=koreanname,
                user=user,
            )
            course.save()
            
    def deletealltaken(self, user):
        for course in TakenCourse.objects.filter(user=user):
            course.delete()
    
def getcleantext(text):
    text = text.replace('&nbsp;', '')
    cleantext = BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
    if not cleantext:
        return ' '
    return cleantext
        

"""
X0  Number
√1  Dept
-2  Code
3  Section
√4  Classif
√5  Title
6  LectureHr
7  LabHr
√8  Credits
√9  AU
10 Retaking
11 Grade
12 Korean 
"""