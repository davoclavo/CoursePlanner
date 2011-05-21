# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from CoursePlanner.models import *
from CoursePlanner.forms import *
from django.template import RequestContext
from scrapers import kaipa, mail
from django.contrib.auth.models import User
from django.contrib import auth

def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            taker = kaipa.session(username,password)
            # Check if credentials match KAIPA's
            correct = taker.login()
            if correct:
                user, dummy = User.objects.get_or_create(username=username)
                
                #Login the user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)                
                
                taker.takecourses()
                user = taker.takeuserinfo()
                request.session['users'] = user
                request.session['kaipa'] = taker
                
                print '--%s(%s)[%s] is an %s from %s'%(user.name,user.number,user.status,user.program,user.department)
                return redirect('/CoursePlanner')
            else:
                return HttpResponse('Wrong ID and password combination')
    else:
        form = LoginForm()

    return render_to_response('login.html', {
        'form': form,},
        context_instance=RequestContext(request)
    )

def main(request):
    if request.user.is_authenticated():
        user = request.session['users']
        alltaken = TakenCourse.objects.filter(user=request.user)
        taken = alltaken.exclude(grade='R').exclude(grade='W')
        totalcredits = {'GM': 0, 'GE': 0, 'BM': 0, 'BE': 0, 'MM': 0, 'ME': 0, 'OE': 0, 'OO': 0, 'RR': 0, 'TOTAL': 0}
        
#         GM - General Mandatory
#         GE - General Elective
#         BM - Basic Mandatory
#         BE - Basic Elective
#         MM - Major Mandatory
#         ME - Major Elective
#         OE - Other Elective
#         OO - Other Other - If the course tagger fails to find a suitable type
#         RR - Research
#         TOTAL - Total Credits
        
        type = ''
        for course in taken:
            type = course.classification[0] + course.type[0]
            if 'F' not in course.grade and 'R' not in course.grade: # Do not add credits if the course was failed or retaken
                totalcredits[type] += course.credits
                totalcredits['TOTAL'] += course.credits

        GM = taken.filter(user=request.user, classification='General', type='Mandatory')
        GE = taken.filter(user=request.user, classification='General', type='Elective')
        BM = taken.filter(user=request.user, classification='Basic', type='Mandatory')
        BE = taken.filter(user=request.user, classification='Basic', type='Elective')
        MM = taken.filter(user=request.user, classification='Major', type='Mandatory')
        ME = taken.filter(user=request.user, classification='Major', type='Elective')
        OE = taken.filter(user=request.user, classification='Other', type='Elective')
        OO = taken.filter(user=request.user, classification='Other', type='Other')
        RR = taken.filter(user=request.user, classification='Research')
        
        requirements = Requirement.objects.get(dept=user.department)
        
        alloffered = OfferedCourse.objects.all()
        suggested = alloffered
        
        passed = taken.exclude(grade='F').exclude(grade='W') # It will suggest a course if you have failed it
        
        for course in passed:
            suggested = suggested.exclude(code=course.code)
        if 'Undergraduate' in user.program:
            suggested = suggested.exclude(code__contains='.5').exclude(code__contains='.6').exclude(code__contains='.7').exclude(code__contains='.8').exclude(code__contains='.9')
        if 'Master' in user.program:
            suggested = suggested.exclude(code__contains='.1').exclude(code__contains='.2').exclude(code__contains='.3')
        
        suggested = suggested.order_by('code')
        SGM = 0
        SGE = 0
        SBM = 0
        SBE = 0
        SMM = 0
        SME = 0
        SOE = 0
        SOO = 0
        SRR = 0
        if(totalcredits['GM'] < requirements.GM):
            SGM = suggested.filter(classification='General', type='Elective')
        if(totalcredits['GE'] < requirements.GE):
            SGE = suggested.filter(classification='General', type='Elective')
        if(totalcredits['BM'] < requirements.BM):
            SBM = suggested.filter(classification='Basic', type='Mandatory')
        if(totalcredits['BE'] < requirements.BE):
            SBE = suggested.filter(classification='Basic', type='Elective')
        if(totalcredits['MM'] < requirements.MM):
            SMM = suggested.filter(classification='Major', type='Mandatory', dept=user.department)
        if(totalcredits['ME'] < requirements.ME):
            SME = suggested.filter(classification='Major', type='Elective', dept=user.department)
        if(totalcredits['OE'] < requirements.OE):
            SOE = suggested.filter(classification='Other', type='Elective')
        if(totalcredits['OO'] < requirements.OO):
            SOO = suggested.filter(classification='Other', type='Other')
        if(totalcredits['RR'] < requirements.RR):
            SRR = suggested.filter(classification='Research')
        
        return render_to_response(
            'main.html',{
            'user': user,
            'requirements': requirements,
            'GM': GM,
            'GE': GE,
            'BM': BM,
            'BE': BE,
            'MM': MM,
            'ME': ME,
            'OE': OE,
            'OO': OO,
            'RR': RR,
            'GM_Credits': totalcredits['GM'],
            'GE_Credits': totalcredits['GE'],
            'BM_Credits': totalcredits['BM'],
            'BE_Credits': totalcredits['BE'],
            'MM_Credits': totalcredits['MM'],
            'ME_Credits': totalcredits['ME'],
            'OE_Credits': totalcredits['OE'],
            'OO_Credits': totalcredits['OO'],
            'RR_Credits': totalcredits['RR'],
            'TOTAL': totalcredits['TOTAL'],
            'SGM': SGM,
            'SGE': SGE,
            'SBM': SBM,
            'SBE': SBE,
            'SMM': SMM,
            'SME': SME,
            'SOE': SOE,
            'SOO': SOO,
            'SRR': SRR,
            }
        )
    else:
        return HttpResponseRedirect('/')
    
def logout_page(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def all(request):
    courses = OfferedCourse.objects.all()
    return render_to_response(
        'all.html',{
        'courses': courses
        }
    )
    
def sms(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = SMSForm(request.POST)
            if form.is_valid():
                username = request.session['kaipa'].username
                password = request.session['kaipa'].password
                sender = mail.session(username, password)
                fromhp = form.cleaned_data['fromhp']
                tohp = form.cleaned_data['tohp']
                msg = form.cleaned_data['msg']
                print('From: ' + fromhp + ' - To: ' + tohp + ' - Msg: ' + msg)
                sender.sendsms(fromhp,tohp,msg)
        else:
            form = SMSForm()
        return render_to_response('sms.html', {
            'form': form,},
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect('/')
        

        
        