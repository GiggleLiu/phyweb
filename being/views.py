#-*-coding:utf-8-*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from gweb.views import showerrorpage
from being import forms
from being.models import *
from notice.models import newnotice
from datetime import date
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group,Permission
from django.template import RequestContext
from django.http import HttpResponseRedirect
import datetime

# Create your views here.
#################################################################### user related views #################################

def user_detail(request,userid):
    if request.method=='GET':
        context=RequestContext(request)
        objuser=getuser(userid)
        being=getbeingbyuser(objuser)
        return render_to_response('user_detail.html',{'objectbeing':being},context)

@login_required
def user_call(request,uid):
    if request.method=='GET':
        targetuser=getuser(uid)
        mailcall(targetuser)
        return HttpResponseRedirect("/being/user_detail/"+uid)

@csrf_exempt
def login(request):
    context=RequestContext(request)
    if request.method=='POST':
        #check that the test cookie worked.
        user=auth.authenticate(username=request.POST.get('username'),password=request.POST.get('password'))
        if user:
            if user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                print 'login!'
                return HttpResponseRedirect("/")
            else:
                return render_to_response('index.html',{'error':'your account is no longer active!'},context)
        else:
            print 'authentication failure'
            return render_to_response('index.html',{'error':'Password incorrect!'},context)

    #request.session.set_test_cookie()
    return render_to_response('index.html',context)

@csrf_exempt
def register_step2(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    if request.method == 'GET':
        user_form = forms.UpdateBeingForm()
        return render_to_response('being_update.html',{'form':user_form},context)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        profile_form = forms.NewBeingForm(data=request.POST)
        uid=request.session.get('userid')
        if uid:
            user=getuser(uid)
        else:
            user=request.user
        
        if user!=None:
            if profile_form.is_valid():
                # Did the user provide a profile picture?
                # If so, we need to get it from the input form and put it in the UserProfile model.
                face = request.FILES.get('face')
                data=profile_form.cleaned_data
                being=newbeing(user,birthday=data['birthday'],gender=data['gender'],truename=data['truename'],telephone=data['telephone'],qq=data['qq'],weixin=data['weixin'],description=data['description'],weibo=data['weibo'],face=face)
    
                # Now we save the UserProfile model instance.
                return HttpRedirect('/being/register_success/')
            else:
                error=profile_form.errors
        else:
            error='invalid request, 1. check your current status. 2. return to step1. 3.maybe some system error,please contact the website manager.'
    return render_to_response('being_update.html',{'error': error},context)

def register_success(request):
    context = RequestContext(request)
    return render_to_response('success.html',{'content': '恭喜你，成功注册了本站，您现在可以在遵守GNU协议的基础上，使用本站!'},context)

@csrf_exempt
def register_step1(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    if request.method == 'GET':
        return render_to_response('user_update.html',context)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = forms.NewUserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            data=user_form.cleaned_data
            user=newuser(username=data['username'],email=data['email'],password=data['password'])
            request.session['userid']=user.id

            # Update our variable to tell the template registration was successful.
            return HttpResponseRedirect('/being/register_step2/')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            error=user_form.errors

    # Render the template depending on the context.
    return render_to_response('user_update.html',{'error': error},context)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
@login_required
def being_update(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    if request.method == 'GET':
        user=request.user
        being=getbeingbyname(name=user.username)
        user_form = forms.UpdateBeingForm(instance=user.being)
        return render_to_response('being_update.html',{'being':being,'update':True,'form':user_form},context)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = forms.UpdateBeingForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            print 'valid form'
            # Save the user's form data to the database.
            data=user_form.cleaned_data
            user = request.user
            face=None
            if 'face' in request.FILES:
                face = request.FILES['face']

            updatebeing(user,face=face,birthday=data['birthday'],truename=data['truename'],description=data['description'],gender=data['gender'],qq=data['qq'],telephone=data['telephone'],weixin=data['weixin'],weibo=data['weibo'])

            # Update our variable to tell the template registration was successful.
            return HttpResponseRedirect('/being/user_detail/'+str(user.id))

        else:
            error='invalid form, please check your input.'
            print 'invalid form'

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        error='Error accur'

    # Render the template depending on the context.
    return render_to_response(
            'user_update.html',
            {'error': error},
            context)


@csrf_exempt
@login_required
def user_update(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    if request.method == 'GET':
        user=request.user
        being=getbeingbyname(name=user.username)
        return render_to_response('user_update.html',{'being':being,'update':True},context)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        print 'get data'
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = forms.UpdateUserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            data=user_form.cleaned_data
            # Save the user's form data to the database.
            user = request.user
            updateuser(user,data['oldpassword'],data['password'],data['email'])

            # Update our variable to tell the template registration was successful.
            return HttpResponseRedirect('/being/user_detail/'+str(user.id))

        else:
            error=user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        error='Error accur'

    # Render the template depending on the context.
    return render_to_response(
            'user_update.html',
            {'error': error},
            context)

@csrf_exempt
@login_required
def update_password(request):
    context = RequestContext(request)
    if request.method == 'POST':
        passwordform = forms.UpdatePasswordForm(data=request.POST)
        if passwordform.is_valid():
            old=request.POST.get('oldpassword')
            new=request.POST.get('newpassword')
            # Save the user's form data to the database.
            user=auth.authenticate(username=request.user.username,password=old)
            if user:
                user.set_password(new)
                print user.username,' password changed!'
                user.save()
                # Update our variable to tell the template registration was successful.
                return HttpResponseRedirect('/being/user_detail/'+str(user.id))
            else:
                error='initial password incorrect!'

        else:
            error='invalid form, please check your input.'

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        error='Error accur, accept only post data!.'

    # Render the template depending on the context.
    return render_to_response(
            'user_update.html',
            {'error': error},
            context)

def user_delete(request):
    context = RequestContext(request)
    if request.method == 'GET':
        user=request.user
        deleteuser(user)
        return HttpResponseRedirect('/')

