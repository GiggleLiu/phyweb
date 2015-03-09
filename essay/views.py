#-*-coding:utf-8-*-
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from essay import forms
from essay.models import *


# Create your views here.
def topic_list(request,pageindex):
    context=RequestContext(request)
    if pageindex==u'':
        pageindex=1
    pageindex=int(pageindex)
    topiclist,totalpages=gettopiclist(pageindex)
    return render_to_response('topic_list.html',{'topiclist':topiclist,'totalpages':totalpages,'pageindex':pageindex},context)

@login_required
@csrf_exempt
def topic_new(request):
    context=RequestContext(request)
    if not request.user.has_perm('being.can_add_topic'):
        return render_to_response('topic_list.html',{'error':'You Have No Permission to Add a Topic!'},context)
    if request.method=='POST':
        cform=forms.NewTopicForm(data=request.POST)
        if cform.is_valid():
            data=cform.cleaned_data
            newtopic(**data)
            return HttpResponseRedirect('/topic/1/')
    else:
        return render_to_response('topic_new.html',{'form':forms.NewTopicForm},context)

@login_required
@csrf_exempt
def topic_update(request,tid):
    context=RequestContext(request)
    if not request.user.is_superuser:
        return render_to_response('topic_list.html',{'error':'You Have No Permission to Update a Topic!'},context)
    if request.method=='POST':
        cform=forms.UpdateTopicForm(data=request.POST)
        if cform.is_valid():
            data=cform.cleaned_data
            updatetopic(tid=tid,**data)
            return HttpResponseRedirect('/topic/')
    else:
        return render_to_response('topic_new.html',{'form':forms.UpdateTopicForm(),'update':True,'tid':tid},context)

@login_required
def topic_delete(request,tid):
    context=RequestContext(request)
    if not request.user.is_superuser:
        return render_to_response('topic_list.html',{'error':'You Have No Permission to Update a Topic!'},context)
    if request.method=='GET':
        deletetopic(tid)
        return render_to_response('topic_list.html',{'info':'Delete Success!'},context)


def essay_list(request,tid,pageindex):
    context=RequestContext(request)
    pageindex=int(pageindex)
    essaylist,totalpages=getessaybytopic(tid,pageindex)
    return render_to_response('essay_list.html',{'topic':gettopic(tid),'essaylist':essaylist,'totalpages':totalpages,'pageindex':pageindex},context)

def user_blog(request,uid,pageindex):
    context=RequestContext(request)
    pageindex=int(pageindex)
    essaylist,totalpages=getessaybyuser(uid,pageindex)
    return render_to_response('essay_list.html',{'essaylist':essaylist,'totalpages':totalpages,'pageindex':pageindex,'targetuser':getuser(uid)},context)

def essay_detail(request,eid):
    context=RequestContext(request)
    essay=getessay(eid)
    return render_to_response('essay_detail.html',{'essay':essay},context)

@login_required
@csrf_exempt
def essay_new(request,tid,content_type):
    if request.method=='GET':
        context=RequestContext(request)
        form=forms.EssayAdminForm()
        topic=gettopic(tid)
        if content_type=='default':
            content_type=topic.default_content_type
        return render_to_response('essay_editor.html',{'form':form,'update':False,'topic':topic,'content_type':content_type},context)

    if request.method=='POST':
        esform = forms.NewEssayForm(data=request.POST)
        topic=gettopic(tid)
        if esform.is_valid():
            data=esform.cleaned_data
            user=request.user
            es=newessay(user,data['title'],data['content'],topic=topic,content_type=data['content_type'])
            return HttpResponseRedirect('/topic/essay/detail/'+str(es.id))
        else:
            print esform.errors
            return HttpResponseRedirect('/essay/fail_submit/')
    else:
        return HttpResponseRedirect("/")

def fail_submit(request):
    if request.method=='GET':
        context=RequestContext(request)
        return render_to_response('errorpage.html',{'error':'提交失败！请检查您的输入内容是否为空。'},context)

@login_required
@csrf_exempt
def essay_update(request,eid):
    if request.method=='POST':
        if not request.user.has_perm('being.can_edit_essay'):
            return HttpResponseRedirect('/topic/1/')

        esform = forms.UpdateEssayForm(data=request.POST)
        if esform.is_valid():
            data=esform.cleaned_data
            user=request.user
            updateessay(eid,data['title'],data['content'])
            return HttpResponseRedirect('/topic/essay/detail/'+str(eid)+'/')
        else:
            print esform.errors
    else:
        context=RequestContext(request)
        essay=getessay(eid)
        form=forms.EssayAdminForm(instance=essay)
        return render_to_response('essay_editor.html',{'form':form,'update':True,'topic':essay.topic,'essay':essay,'content_type':essay.content_type},context)

@login_required
@csrf_exempt
def essay_delete(request,eid):
    if request.method=='GET':
        essay=getessay(eid)
        topic=essay.topic
        if request.user.has_perm('being.can_edit_essay'):
            deleteessay(eid)
        return HttpResponseRedirect('/topic/essay/list/'+str(topic.id)+'/1/')

@login_required
def essay_edit(request,block,title):
    if request.method=='GET':
        if request.user.has_perm('being.can_edit_essay'):
            context=RequestContext(request)
            essay=getessaybytitle(block,title)
            update=False if essay==None else True
            #update=False #use this line to make a copy of older version available.
            from essay.forms import EssayAdminForm
            form=EssayAdminForm(instance=essay)
            titlelist=gettitlesofblock(block)
            return render_to_response(block+'_editor.html',{'essay':essay,'form':form,'update':update,'titlelist':titlelist,'blk':block},context)
        else:
            return HttpResponseRedirect('/'+block+'/')
