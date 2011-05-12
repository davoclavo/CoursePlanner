from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OfferedCourse(models.Model):
    number = models.IntegerField(primary_key=True) #number from the list of total course
    dept = models.CharField(max_length=200) #department
    classification = models.CharField(max_length=200) #type of course, eg. elective, mandatory
    coursenum = models.CharField(max_length=200) #Dept+course ID, eg. CS480
    section = models.CharField(max_length=200) #Which group from that course
    code = models.CharField(max_length=200) #Unique code
    title = models.CharField(max_length=200) #Title
    llc = models.CharField(max_length=200) #Lecture hours - Lab hours - Credits 
    schedule = models.CharField(max_length=200) #Time table
    room = models.CharField(max_length=200) #Room of the class
    fixednum = models.CharField(max_length=200) #Max number of students?
    remarks = models.CharField(max_length=200) #Extra comments, eg. English
    
class TakenCourse(models.Model):
    number = models.IntegerField() #number from the list of total course
    dept = models.CharField(max_length=100) #department
    #section = models.CharField(max_length=200) #Which group from that course
    code = models.CharField(max_length=15) #Unique code
    classification = models.CharField(max_length=100) #type of course, eg. elective, mandatory
    title = models.CharField(max_length=100) #Title
    grade = models.CharField(max_length=4) #Grade
    koreanname = models.CharField(max_length=100) #Korean name
    user = models.ForeignKey(User)