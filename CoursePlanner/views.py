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
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)                
                
                taker.takecourses()
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
    courses = TakenCourse.objects.filter(user=request.user)
    return render_to_response(
        'taken.html',{
        'courses': courses
        }
    )
