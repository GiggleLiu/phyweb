#!/usr/bin/python
#-*-coding:utf-8-*-
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse,Http404
from being.models import getmemberlist,getgroup
from django.template.loader import get_template
import pdb

from django_comments.views.moderation import perform_delete
from django_comments.models import Comment

def gethelp(request,topic):
    context = RequestContext(request)
    return render_to_response('help_'+topic+'.html',{},context)

def mainpage(request):
    context=RequestContext(request)
    return render_to_response('index.html',{},context)

def login(request):
    context=RequestContext(request)
    return render_to_response('index.html',{'login':True},context)

def page_not_found(request):
    context=RequestContext(request)
    return render_to_response('404.html',{},context)
   
def page_error(request):
    context=RequestContext(request)
    return render_to_response('500.html',{},context)

def showerrorpage(request,message):
    context=RequestContext(request)
    return render_to_response('errorpage.html',{'error':message},context)

def delete_own_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment.user.id != request.user.id and (not request.user.has_perm('being.can_edit_essay')) and (not request.user.has_perm('being.can_delete_essay')):
        raise Http404
    perform_delete(request, comment)
    es=comment.content_object
    return HttpResponseRedirect('/'+es.block+'/'+es.title+'/')

def latex(request):
    return render_to_response('latex.html',{})
