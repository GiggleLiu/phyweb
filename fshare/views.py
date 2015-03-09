from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from fshare import forms
from fshare.models import *
from gweb.views import showerrorpage


# Create your views here.
@login_required
@csrf_exempt
def file_new(request):
    if request.method=='POST':
        user=request.user
        flist=request.FILES.getlist('file')
        if not flist:
            context=RequestContext(request)
            return render_to_response('errorpage.html',{'error':'no files attached'},context)
        for f in flist:
            newfile(user,f,description=request.POST.get('description'))
    return HttpResponseRedirect("/inner/file/")


@login_required
@csrf_exempt
def file_delete(request,eid):
    if request.method=='GET':
        deletefile(eid)
        return HttpResponseRedirect("/inner/file/")
