# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from CoursePlanner.models import *
from CoursePlanner.forms import *
from django.template import RequestContext
from scrapers import kaipa
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
                taker.takeuserinfo()
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
        total = 0
        GM = TakenCourse.objects.filter(user=request.user, classification='General', type='Mandatory')
        GM_Credits = 0
        for c in GM:
            GM_Credits += c.credits
        total += GM_Credits
        GE = TakenCourse.objects.filter(user=request.user, classification='General', type='Elective')
        GE_Credits = 0
        for c in GE:
            GE_Credits += c.credits
        total += GE_Credits
        BM = TakenCourse.objects.filter(user=request.user, classification='Basic', type='Mandatory')
        BM_Credits = 0
        for c in BM:
            BM_Credits += c.credits
        total += BM_Credits
        BE = TakenCourse.objects.filter(user=request.user, classification='Basic', type='Elective')
        BE_Credits = 0
        for c in BE:
            BE_Credits += c.credits
        total += BE_Credits
        MM = TakenCourse.objects.filter(user=request.user, classification='Major', type='Mandatory')
        MM_Credits = 0
        for c in MM:
            MM_Credits += c.credits
        total += MM_Credits
        ME_Credits = 0
        ME = TakenCourse.objects.filter(user=request.user, classification='Major', type='Elective')
        for c in ME:
            ME_Credits += c.credits
        total += ME_Credits
        OE = TakenCourse.objects.filter(user=request.user, classification='Other', type='Elective')
        OE_Credits = 0
        for c in OE:
            OE_Credits += c.credits
        total += OE_Credits
        OO = TakenCourse.objects.filter(user=request.user, classification='Other', type='Other')
        OO_Credits = 0
        for c in OO:
            OO_Credits += c.credits
        total += OO_Credits
        RR = TakenCourse.objects.filter(user=request.user, classification='Research')
        RR_Credits = 0
        for c in RR:
            RR_Credits += c.credits
        total += RR_Credits
        # HELLO ZACK
        return render_to_response(
            'index.html',{
            'GM': GM,
            'GE': GE,
            'BM': BM,
            'BE': BE,
            'MM': MM,
            'ME': ME,
            'OE': OE,
            'OO': OO,
            'RR': RR,
            'GM_Credits': GM_Credits,
            'GE_Credits': GE_Credits,
            'BM_Credits': BM_Credits,
            'BE_Credits': BE_Credits,
            'MM_Credits': MM_Credits,
            'ME_Credits': ME_Credits,
            'OE_Credits': OE_Credits,
            'OO_Credits': OO_Credits,
            'RR_Credits': RR_Credits,
            'total': total,
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
        'home.html',{
        'courses': courses
        }
    )