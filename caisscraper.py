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
    term = 2 #1-Spring 2-Summer 3-Fall 4-Winter
    offset = 0
    totalcourses = []
    while True:
        pagecourses = scrapecourses(year,term,offset)
        if pagecourses is -1:
            break
        totalcourses += pagecourses
        offset += 7 # totalcourses[-1].number #Increase the offset by the 'number' of the last course scraped
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
        number = int(coursestable[itera*13+0].text)
        dept = coursestable[itera*13+1].text
        classification = coursestable[itera*13+2].text
        coursenum = coursestable[itera*13+3].text
        section = coursestable[itera*13+4].text
        code = coursestable[itera*13+5].text
        title = coursestable[itera*13+6].text
        llc = coursestable[itera*13+7].text
        schedule = coursestable[itera*13+8].text
        room = coursestable[itera*13+9].text
        fixednum = coursestable[itera*13+10].text
        remarks  = coursestable[itera*13+11].text
        course = OfferedCourse(
            number=number,
            dept=dept,
            classification=classification,
            coursenum=coursenum,
            section=section,
            code=code,
            title=title,
            llc=llc,
            schedule=schedule,
            room=room,
            fixednum=fixednum,
            remarks=remarks
        )
        courses.append(course)
        course.save()
        print str(number) + " - " + title
    return courses
            
#XPath: /html/body/table/tbody/tr[14]/td/div/table/tbody/tr[2]
   

if __name__ == '__main__':
    main()