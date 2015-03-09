#-*-coding:utf-8-*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from notice.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponseRedirect
from being.models import getadmin,getgroupuser,getuserbyname
import datetime

# Create your views here.
#################################################################### user related views #################################
@login_required
def messagebox(request,pageindex):
    if request.method=='GET':
        context=RequestContext(request)
        pageindex=int(pageindex)
        nl,hasnext=getnoticelist(request.user,pageindex)
        haspre=False if pageindex==1 else True
        res=render_to_response('message_list.html',{'noticelist':nl,'hasnext':hasnext,'haspre':haspre,'pageindex':pageindex},context)
        readnotices(nl)
        return res

@csrf_exempt
def notice_advice(request):
    if request.method == 'POST':
        sendto=request.POST.get('sendto')
        if sendto=='admin':
            newnotice(getadmin(),u'【建议反馈】 '+request.POST.get('content'))
        elif sendto=='group':
            newnotice(getgroupuser(),u'【收到给本组的留言】'+request.POST.get('content'))
        else:
            try:
                newnotice(getuserbyname(sendto),u'【收到给您的留言】'+request.POST.get('content'))
            except:
                return HttpResponseRedirect('/notice/fail/')
        return HttpResponseRedirect('/notice/success/')

def notice_success(request):
    if request.method=='GET':
        context=RequestContext(request)
        return render_to_response('success.html',{'content':'提交成功！'},context)

def notice_fail(request):
    if request.method=='GET':
        context=RequestContext(request)
        return render_to_response('errorpage.html',{'error':'提交失败！'},context)
