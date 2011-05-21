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
        _user, dummy = User.objects.get_or_create(username=self.username)
        self.user = _user
        
        
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

        
        self.deletealltaken()

        for coursetaken in coursestaken:
            dept = getcleantext(coursetaken[1].text)
            code = getcleantext(coursetaken[2].text)
            #section = getcleantext(coursetaken[3].text)
            fullclassification = getcleantext(coursetaken[4].text)
            classification = fullclassification
            title = getcleantext(coursetaken[5].text)
            #code = ':)'
            
            credits = int(coursetaken[8].text.replace('.0',''))
            au =  int(coursetaken[9].text)
            grade = getcleantext(coursetaken[11].text)
            koreanname = getcleantext(coursetaken[12].text)
            #print "'%s', '%s' , '%s' , '%s' , '%s' , '%s' , '%s'" % (number, dept, code, classification, title, grade, koreanname)
            type='UNKNOWN'
            if classification.find('Mandatory') >= 0 :
                classification = classification.replace('Mandatory','').strip()
                type = 'Mandatory'
                if classification != 'Basic' and classification != 'Major' :
                    classification = 'General'
            elif classification.find('Elective') >= 0 :
                classification = classification.replace('Elective','').strip()
                type = 'Elective'
                if classification != 'Basic' and classification != 'Major' and classification != 'Other':
                    classification = 'General'
            elif classification.find('Required') >= 0 :
                classification = classification.replace('Required','').strip()
                type = 'Mandatory'
                if classification != 'Basic' and classification != 'Major' :
                    classification = 'General'
            elif classification.find('Research') >= 0 or title.find('Research') >= 0  :
                classification = 'Research'
                type = 'Research'
            else:
                classification = 'Other'
                type = 'Other' 
                
            course = TakenCourse(
                dept=dept,
                code=code,
                fullclassification=fullclassification,
                classification=classification,
                title=title,
                credits=credits,
                au=au,
                grade=grade,
                koreanname=koreanname,
                user=self.user,
                type = type,
            )
            course.save()

    def deletealltaken(self):
        TakenCourse.objects.filter(user=self.user).delete()
        
    def takeuserinfo(self):
        url = 'http://kaipa.kaist.ac.kr/menu/hs_menu_eng.jsp'
        req = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(req)
        rawhtml = response.read()
        soup = BeautifulSoup(rawhtml)
        
        name = soup.findAll('td',{'height':'25'}) # Retrieves the name
        number = soup.findAll('option') # Retrieves student ID
        menuitems = soup.findAll('td',{'height':'21'}) # Retrieves the program, department and status
        self.user.name =  getcleantext(name[0].text)
        self.user.number = getcleantext(number[0].text)
        self.user.program = getcleantext(menuitems[0].text)
        self.user.department = getcleantext(menuitems[1].text).replace('Department of','').strip()
        self.user.status = getcleantext(menuitems[2].text)
        return self.user
    
def getcleantext(text):
    text = text.replace('&nbsp;', '')
    cleantext = BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES).text
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