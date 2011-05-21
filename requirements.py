import sys, os
sys.path.append('..')


from django.core.management import setup_environ
from mmk import settings
setup_environ(settings)

from CoursePlanner.models import *


# Department, GM, GE, BM, BE, MM, ME, OE, OO, RR, AU, TOTAL

allreq = [
    ['Civil and Enviromental Engineering',6,21,26,6,9,36,23,0,3,9,130],
    ['Mechanical Engineering',6,21,26,6,9,40,19,0,3,9,130],
    ['Physics',6,21,26,6,19,21,26,0,5,9,130],
    ['Bio & Brain Engineering',6,21,26,6,14,28,0,0,7,9,130],
    ['Industrial & Systems Engineering',6,21,26,6,24,27,0,0,4,9,130],
    ['Industrial Design',6,21,26,6,27,27,0,0,3,9,130],
    #['Biological science',6,,,,,,,0,,9,],
    #['??',6,21,26,6,18,23,,0,4,9,130],
    ['Mathematical Science',6,21,26,6,0,40,0,0,3,9,130],
    ['Nuclear & Quantum Engineering',6,21,26,6,25,18,0,0,3,9,130],
    ['Electrical Engineering',6,21,26,6,18,29,0,0,4,9,130],
    ['Computer Science',6,21,26,6,22,21,0,0,3,9,130],
    ['Aerospace Engineering',6,21,26,9,22,30,0,0,3,9,130],
    ['Chemistry',6,21,26,6,18,24,0,0,3,9,130],
]

#Empty the database
all = Requirement.objects.all()
for req in all:
    req.delete()
    
for deptreq in allreq:
    req = Requirement.objects.create(
        dept = deptreq[0],
        GM = deptreq[1],
        GE = deptreq[2],
        BM = deptreq[3],
        BE = deptreq[4],
        MM = deptreq[5],
        ME = deptreq[6],
        OE = deptreq[7],
        OO = deptreq[8],
        RR = deptreq[9],
        AU = deptreq[10],
        TOTAL = deptreq[11],
        )
