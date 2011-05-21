'''
Created on Apr 19, 2011

@author: David
'''
import sys, os
sys.path.append('..')


from django.core.management import setup_environ
from mmk import settings
setup_environ(settings)


import urllib
from BeautifulSoup import BeautifulSoup
from CoursePlanner.models import *

def main():
    year = 2011
    term = 3 #1-Spring 2-Summer 3-Fall 4-Winter
    offset = 2261
    totalcourses = []
    while True:
        pagecourses = scrapecourses(year,term,offset)
        if pagecourses is -1:
            break
        totalcourses += pagecourses
        offset += 7 # totalcourses[-1].number #Increase the offset by the 'number' of the last course scraped... but cais somehow only shows 7 by 7, so...
    print len(totalcourses)
    
def scrapecourses(year,term,offset):
    baseurl = 'http://webcais.kaist.ac.kr/devsso/lecture/lecture_elist.php?'
    parameters = 'k_status=1&k_year='+str(year)+'&k_term='+str(term)+'&k_dept=-1&k_course=-1&k_subject=-1&offset='+str(offset)
    url = baseurl + parameters
    rawhtml = urllib.urlopen(url).read()
    soup = BeautifulSoup(rawhtml)
    coursestable = soup('td',{'bgcolor' : '#E7E4E4'})
    if len(coursestable) is 0:
        return -1
    courses = []
    for itera in range(0,len(coursestable)/13):

        dept = coursestable[itera*13+1].text.replace('Department of','').strip()
        fullclassification = coursestable[itera*13+2].text
        classification = fullclassification
        coursenum = coursestable[itera*13+3].text
        #section = coursestable[itera*13+4].text
        code = coursestable[itera*13+5].text
        title = coursestable[itera*13+6].text
        llc = coursestable[itera*13+7].text
        credits = llc[-1] # get credits from  l:l:c, so it retrieves the last number
        schedule = coursestable[itera*13+8].text
        room = coursestable[itera*13+9].text
        fixednum = coursestable[itera*13+10].text
        remarks  = coursestable[itera*13+11].text
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
        
        course = OfferedCourse(
            dept=dept,
            fullclassification=fullclassification,
            classification=classification,
            type=type,
            coursenum=coursenum,
            code=code,
            title=title,
            llc=llc,
            credits=credits,
            schedule=schedule,
            room=room,
            fixednum=fixednum,
            remarks=remarks
        )
        courses.append(course)
        course.save()
        
        #DEBUG
        number = int(coursestable[itera*13+0].text)
        print str(number) + ") " + title + "-(" + credits + ")\tClass: " + classification + " Type: " + type + " FULL: " + fullclassification + "   offset: " + str(offset)
    return courses
            
#XPath: /html/body/table/tbody/tr[14]/td/div/table/tbody/tr[2]
   

if __name__ == '__main__':
    main()