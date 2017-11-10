from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from Main.models import Competition, Lecture, User, RegUserForm, LogUserForm
from datetime import datetime
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def home(request):
    CompetitionList = Competition.objects.all()
    if len(CompetitionList) > 5:
        CompetitionList = CompetitionList[0:4]
    LectureList = Lecture.objects.all()
    if len(LectureList) > 5:
        LectureList = LectureList[0:4]
    CompetitionCnt = 0
    LectureCnt = 0
    SlideList = []
    for cnt in range(3):
        if (CompetitionCnt >= len(CompetitionList)) and (LectureCnt >= len(LectureList)):
            break
        if (CompetitionCnt >= len(CompetitionList)):
            SlideList.append(LectureList[LectureCnt])
            LectureCnt += 1
            continue
        if (LectureCnt >= len(LectureList)):
            SlideList.append(CompetitionList[CompetitionCnt])
            CompetitionCnt += 1
            continue
        if (CompetitionList[CompetitionCnt].date_time > LectureList[LectureCnt].date_time):
            SlideList.append(CompetitionList[CompetitionCnt])
            print(CompetitionList[CompetitionCnt].date_time)
            CompetitionCnt += 1
        else:
            SlideList.append(LectureList[LectureCnt])
            print(LectureList[LectureCnt].date_time)
            LectureCnt += 1
    print(LectureCnt)
    print(CompetitionCnt)

    return render(request, 'index.html', {'SlideList': SlideList, 'CompetitionList': CompetitionList, 'LectureList': LectureList})


def competition(request, id):
    return render(request, 'single.html')


def lecture(request, id):
    pass


def competitionList(request):
    return render(request, 'complist.html')


def lectureList(request):
    pass


def login(request):
    if request.method == 'POST':
        uf = LogUserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            userPassJudge = User.objects.filter(username__exact=username,password__exact=password)

            print(User.objects.all())
            if userPassJudge:
                response = HttpResponseRedirect('/index/')
                response.set_cookie('cookie_username',username,3600)
                return response
            else:
                return HttpResponse('No username or valid one')
    else:
        uf = LogUserForm()
    #for test, need to change later.
    return render_to_response('login.html',{'uf':uf})


def register(request):
    Method = request.method
    if Method == 'POST':
        uf = RegUserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password1 = uf.cleaned_data['password1']
            password2 = uf.cleaned_data['password2']
            try:
                registJudge = User.objects.filter(username=username).get().username
                return render_to_response('register.html',{'registJudge':registJudge})
            except :
                if password1 != password2:
                    return HttpResponse('两次密码不一样')

                    registAdd = User.objects.create(username=username,password=password1)
                    #for test, need to change later.
                    return render_to_response('register.html',{'registAdd':registAdd,'username':username})
                elif len(password1)<7:
                    return HttpResponse('Too short password')
                elif password1 == username:
                    return HttpResponse('Username cannot be the same as password.')
                else:
                    registAdd = User.objects.create(username=username,password=password1)
                    #for test, need to change later.
                    return render_to_response('register.html',{'registAdd':registAdd,'username':username})


    else:
        uf = RegUserForm()
    return render_to_response('register.html',{'uf':uf,'Method':Method})

#test login and logout
def index(request):
    username = request.COOKIES.get('cookie_username','')
    return render_to_response('index4test.html',{'username':username})

def logout(request):
    response = HttpResponse('logout!<br><a href="127.0.0.1:8000/regist>register</a>"')
    response.delete_cookie('cookie_username')
    return  response


def slide(request):
    pass
