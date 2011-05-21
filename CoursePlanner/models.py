from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OfferedCourse(models.Model):
    dept = models.CharField(max_length=200) #department
    fullclassification = models.CharField(max_length=200) #full type of course, eg. elective, mandatory
    classification = models.CharField(max_length=200) #type of course, eg. elective, mandatory
    coursenum = models.CharField(max_length=200) #Dept+course ID, eg. CS480
    #section = models.CharField(max_length=200) #Which group from that course
    code = models.CharField(max_length=200, primary_key=True) #Unique code
    title = models.CharField(max_length=200) #Title
    llc = models.CharField(max_length=200) #Lecture hours - Lab hours - Credits 
    schedule = models.CharField(max_length=200) #Time table
    room = models.CharField(max_length=200) #Room of the class
    fixednum = models.CharField(max_length=200) #Max number of students?
    remarks = models.CharField(max_length=200) #Extra comments, eg. English
    type = models.CharField(max_length=15) # Course Type
    credits = models.IntegerField()
    
    
class TakenCourse(models.Model):
    dept = models.CharField(max_length=100) #department
    #section = models.CharField(max_length=200) #Which group from that course
    code = models.CharField(max_length=15) #Unique code
    fullclassification = models.CharField(max_length=200) #full type of course, eg. elective, mandatory
    classification = models.CharField(max_length=100) #type of course, eg. elective, mandatory
    title = models.CharField(max_length=100) #Title
    grade = models.CharField(max_length=4) #Grade
    koreanname = models.CharField(max_length=100) #Korean name
    user = models.ForeignKey(User)
    semester = models.CharField(max_length=100) # Semester in which the course was taken
    type = models.CharField(max_length=15) # Course Type
    credits = models.IntegerField()
    au = models.IntegerField()
    
class Requirement(models.Model):
    dept = models.CharField(max_length=100) #department
    GM = models.IntegerField()
    GE = models.IntegerField()
    BM = models.IntegerField()
    BE = models.IntegerField()
    MM = models.IntegerField()
    ME = models.IntegerField()
    OE = models.IntegerField()
    OO = models.IntegerField()
    RR = models.IntegerField()
    AU = models.IntegerField()
    TOTAL = models.IntegerField()