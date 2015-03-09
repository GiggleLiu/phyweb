#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User,Group,Permission
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.db.models import Q
import datetime,re

# Create your models here.
class Being(models.Model):
    '''define the basic person model'''
    user=models.OneToOneField(User)
    gender=models.CharField(choices=(('male','male'),('female','female')),max_length=16,default='male')
    truename=models.CharField(max_length=32)
    occupation=models.CharField(max_length=32)
    description=models.CharField(null=True,blank=True,max_length=512)
    face=models.ImageField(upload_to='avatar',blank=True,null=True)
    birthday=models.DateField(null=True,blank=True)

    #contact methods
    qq=models.CharField(max_length=16,null=True,blank=True)
    weixin=models.CharField(max_length=32,null=True,blank=True)
    telephone=models.CharField(max_length=32,null=True,blank=True)
    weibo=models.CharField(max_length=32,null=True,blank=True)
    class Meta:
        ordering=['truename']

    def __unicode__(self):
        return u'%s' % (self.truename)

    def link(self):
        return '<a href="/being/user_detail/'+str(self.user.id)+'/">'+self.truename+'</a>'

#about the being
def getuser(uid):
    return User.objects.get(id=uid)
def getbeing(bid):
    return Being.objects.get(id=bid)

def getbeingbyuser(user):
    return Being.objects.get(user=user)

def getbeingbyname(name):
    user=User.objects.get(username=name)
    return Being.objects.get(user=user)

def getuserbyname(name):
    try:
        user=User.objects.get(username=name)
        return user
    except:
        return None

def getrecordlist(user):
    pass
    #l=list(user.clauserecord_set.all())
    #l=l+list(user.creaturerecord_set.all())
    #l=l+list(user.postrecord_set.all())
    #l.sort(key=lambda x:x.happentime,reverse=True)
    #return l

def mailcall(user):
    send_mail('遥远星球的呼叫','有人在星球上呼叫了您，这是一封邮件提醒~',from_email='postmaster@yanglala.com',recipient_list=[user.email])
    return True

def getadmin():
    return getuserbyname('cacate')

def getgroupuser():
    return getuserbyname('group')

def newbeing(user,birthday,gender,truename,description,telephone,qq,weixin,weibo,face):
    being=Being(user=user,gender=gender,truename=truename,telephone=telephone,qq=qq,weixin=weixin,description=description,weibo=weibo,face=face)
    being.save()
    return being

def newuser(username,password,email):
    user=User(username=username,email=email)
    user.set_password(password)
    g=Group.objects.get(name='default')
    user.save()
    user.groups.add(g)
    return user

def deleteuser(uid):
    User.objects.get(pk=uid).delete()
    return True

def updateuser(user,oldpassword,newpassword,email):
    if user.check_password(oldpassword):
        user.email=email
        user.set_password(newpassword)
        user.save()
def updatebeing(user,birthday,gender,truename,description,telephone,qq,weixin,weibo,face):
    being=Being.objects.get(user=user)
    being.gender=gender
    being.truename=truename
    being.telephone=telephone
    being.qq=qq
    being.weixin=weixin
    being.description=description
    being.weibo=weibo
    if face:
        being.face=face
    being.save()
    return being

def getperm(perm):
    try:
        pm=Permission.objects.get(codename=perm)
        return pm
    except:
        return False

def newperm(perm):
    content_type = ContentType.objects.get(app_label='being', model='being')
    pminner=Permission.objects.create(codename=perm,name=perm,content_type=content_type)
    return pminner

def addpermtouser(user,perm):
    getperm(perm)
    user.user_permissions.add(pminner)
    return True

def addpermtogroup(group,perm):
    pminner=getperm(perm)
    group.permissions.add(pminner)
    return True

def getgroup(gname):
    try:
        g=Group.objects.get(name=gname)
        return g
    except:
        return None

def newgroup(gname):
    g=Group(name=gname)
    g.save()
    return g

def ghas_perm(group,perm):
    return group.permissions.filter(codename=perm)

def initialize():
    #init permissions
    if not getperm('can_edit_essay'):
        newperm('can_edit_essay')
    if not getperm('can_audit_essay'):
        newperm('can_audit_essay')
    if not getperm('can_add_topic'):
        newperm('can_add_topic')


    #init group
    gdefault=getgroup('default')
    if not gdefault:
        gdefault=newgroup('default')
    gmanager=getgroup('manager')
    if not gmanager:
        gmanager=newgroup('manager')

    #init user
    if not getuserbyname('admin'):
        newuser('admin','liujinguo','cacate0129@gmail.com')

    #set can_visit_inner permission
    if not ghas_perm(gdefault,'can_edit_essay'):
        addpermtogroup(gdefault,'can_edit_essay')
    if not ghas_perm(gmanager,'can_edit_essay'):
        addpermtogroup(gmanager,'can_edit_essay')
    if not ghas_perm(gmanager,'can_audit_essay'):
        addpermtogroup(gmanager,'can_audit_essay')
    if not ghas_perm(gmanager,'can_add_topic'):
        addpermtogroup(gmanager,'can_add_topic')
    return True

def getmemberlist():
    gs=set(getgroup('student').user_set.all())
    gp=set(getgroup('professor').user_set.all())
    gs.update(gp)
    ulist=[user for user in gs if hasattr(user,'being')]
    blist=[user.being for user in ulist]
    return blist
