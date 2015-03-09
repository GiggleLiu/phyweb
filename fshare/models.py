from django.db import models
from django.contrib.auth.models import User,Group,Permission
import datetime

# Create your models here.
class Fshare(models.Model):
    f=models.FileField(upload_to='fshare')
    creater=models.ForeignKey(User,null=True,blank=True)
    description = models.CharField(max_length=128,null=True,blank=True)
    uploadtime=models.DateTimeField(default=datetime.datetime.now)
    tag = models.CharField(max_length=32,null=True,blank=True)
    class Meta:
        ordering=['-uploadtime']

    def __unicode__(self):
        filename=self.f.name.split('/')[-1]
        return u'%s' % (filename)

    def link(self):
        return '<a href="'+str(self.f.url)+'/">'+self.__unicode__()+'</a>'

def newfile(user,f,description):
    fs=Fshare(creater=user,f=f,description=description)
    fs.save()
    return fs

def getfile(fid):
    return Fshare.objects.get(pk=fid)

def deletefile(fid):
    getfile(fid).delete()
    return True

def getfiles():
    return Fshare.objects.all()
