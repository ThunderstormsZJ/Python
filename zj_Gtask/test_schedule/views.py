from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from test_schedule.models import Schedule

# Create your views here.
ONE_PAGE_OF_DATA = 5  
def sche_list(request):
    try:
        curpage = int(request.GET.get('curpage',1))
        pagetype = request.GET.get('pagetype','')
        if pagetype=='':
            pagetype=''
    except ValueError:
        curpage = 1
        pagetype = ''

    allrecord = Schedule.objects.count()
    allpage = (allrecord+ONE_PAGE_OF_DATA-1)//ONE_PAGE_OF_DATA
    
    if pagetype=='pageUp':
        curpage -= 1
    elif pagetype=='pageDown':
        curpage += 1
        
    if pagetype=='pageBef' or curpage<1:
        curpage = 1
    if pagetype=='pageLat' or curpage>allpage:
        curpage = allpage
        
    startpos = (curpage-1)*ONE_PAGE_OF_DATA
    endpos = startpos + ONE_PAGE_OF_DATA
    
    if endpos>allrecord:
        endpos = allrecord
    print("---------------------")
    print(startpos)
    schedules = Schedule.objects.all()[startpos:endpos]
    
    return render_to_response('schedule_list.html',
                              {'schedules':schedules,'allrecord':allrecord,'allpage':allpage,'curpage':curpage})

def sche_add(request):
    return render_to_response('schedule_edit.html')

@csrf_exempt
def sche_add_oper(request):
    if request.POST:
        title = request.POST['title']
        content = request.POST['content']
        id = request.POST['id']
        print(type(id))
        if id=='':
            schedule = Schedule(title=title,content=content)
            schedule.save()
            print('id-->%s' % schedule.id)
            return HttpResponse("success")
        else:
            schedule = Schedule.objects.get(id=id)
            schedule.title = title
            schedule.content = content
            schedule.save()
            return HttpResponse("success")
    else:
        return HttpResponse("fail")

@csrf_exempt
def sche_delby_id(request,id):
    schedule = Schedule.objects.get(id=id)
    schedule.delete()
    return HttpResponseRedirect('/sche_list')

@csrf_exempt
def sche_delby_ids(request):
    if request.POST:
        ids = request.POST['allIDCheck']
        idArr = ids.split(',')
        for id in idArr:
            schedule = Schedule.objects.get(id=id)
            schedule.delete()
        return HttpResponseRedirect('/sche_list')
    else:
        return HttpResponse("fail")

def sche_edit(request,id):
    schedule = Schedule.objects.get(id=id)
    return render_to_response('schedule_edit.html',{'schedule':schedule})
