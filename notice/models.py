#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User
import datetime,re
from being.models import getadmin,getgroupuser
from django.db.models import Q

class Notice(models.Model):
    '''the record of the the law'''
    user=models.ForeignKey(User)
    content=models.CharField(max_length=512)
    ctime=models.DateTimeField(default=datetime.datetime.now)
    status=models.CharField(max_length=512,default='unread') #unread/read

    class Meta:
        ordering=['-ctime']

#about the notice
def getnotice(nid):
    return Notice.objects.get(id=nid)

def getnoticelist(user,pageindex):
    '''return the list and wether it has next page'''
    nl=Notice.objects.filter(Q(user=user)|Q(user=getgroupuser()))
    if len(nl)>pageindex*20:
        nl20=nl[(pageindex-1)*20:pageindex*20]
        return nl20,True
    elif len(nl)>(pageindex-1)*20:
        nl20=nl[(pageindex-1)*20:]
        return nl20,False
    else:
        return None,False

def readnotices(nl):
    if not nl:
        return
    for n in nl:
        if n.status!='read':
            n.status='read'
            n.save()
    return True

def deletenotice(nid):
    n=getnotice(nid)
    n.delete()
    return True

def newnotice(user,content):
    n=Notice(user=user,content=content)
    n.save()
    return n

def getunreadnoticecount(user):
    groupmescount=Notice.objects.filter(user=getgroupuser(),status='unread').count()
    return Notice.objects.filter(user=user,status='unread').count()+groupmescount
