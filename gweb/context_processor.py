from notice.models import getunreadnoticecount
def myprocessor(request):
    ns=[0,0,0]#getnoticestatus(request.user)
    if request.user.is_authenticated():
        ns[0]=getunreadnoticecount(request.user)
    context = {'noticestatus': ns}

    return context
