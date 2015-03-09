from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User,Group,Permission
import datetime
from gweb.utils import pagerget

# Create your models here.
class Topic(models.Model):
    '''topic of essay.'''
    LATEX='latex'
    CKEDITOR='ckeditor'
    EDITORS=((LATEX,'latex'),(CKEDITOR,'ckeditor'))
    title=models.CharField(max_length=128,unique=True)
    description=models.CharField(null=True,blank=True,max_length=1024)
    default_content_type=models.CharField(max_length=32,choices=EDITORS,default=CKEDITOR)

    def __unicode__(self):
        return u'%s'%(self.title)

    def link(self):
        return '<a href="/topic/essay/list/'+str(self.id)+'/1/">'+self.__unicode__()+'</a>'

class Essay(models.Model):
    title=models.CharField(max_length=128)
    author=models.ForeignKey(User,null=True,blank=True)
    content = RichTextField(null=True,blank=True)
    backup = RichTextField(null=True,blank=True)
    updatetime=models.DateTimeField(default=datetime.datetime.now)
    topic=models.ForeignKey(Topic)
    content_type=models.CharField(max_length=32,default='latex')
    class Meta:
        ordering=['-updatetime']

    def __unicode__(self):
        return u'%s' % (self.title)

    def link(self):
        return '<a href="/topic/essay/detail/'+str(self.id)+'/">'+self.__unicode__()+'</a>'

    def update(self,content):
        self.content=content
        self.save()
        return True


def newessay(user,title,content,topic,content_type):
    es=Essay(author=user,title=title,content=content,topic=topic,content_type=content_type)
    es.save()
    return es

def updateessay(eid,title=None,content=None):
    es=getessay(eid)
    if content!=None:
        es.backup=es.content
        es.content=content
    if title!=None:
        es.title=title
    es.save()

def getessay(eid):
    return Essay.objects.get(pk=eid)

def getessaybytopic(topicname,pageindex):
    el=gettopic(topicname).essay_set.all()
    return pagerget(el,pageindex)

def gettopicbyname(topicname):
    return Topic.objects.get(title=topicname)

def gettopic(tid):
    return Topic.objects.get(pk=tid)

def newtopic(**kwargs):
    bl=Topic(title=kwargs.get('title'),description=kwargs.get('description'),default_content_type=kwargs.get('default_content_type'))
    bl.save()
    return bl

def deletetopic(tid):
    gettopic(tid).delete()
    return True

def updatetopic(tid,**kwargs):
    tp=gettopic(tid)
    tp.title=kwargs.get('title')
    tp.desciption=kwargs.get('desciption')
    tp.default_content_type=kwargs.get('default_content_type','latex')
    tp.save()
    return True

def deleteessay(eid):
    getessay(eid).delete()
    return True

def gettopiclist(pageindex):
    tps=Topic.objects.all()
    return pagerget(tps,pageindex)
