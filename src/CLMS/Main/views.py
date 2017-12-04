from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from Main.models import *
from datetime import datetime
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
import hashlib
# from django.views.decorators.csrf import csrf_exempt
# from Main.wxapp import WxApp
# Create your views here.


class RegUserForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'username or email',
                                   'id': 'reg_username'
                               }))
    password1 = forms.CharField(label='密码',
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'password(>6 letters)',
                                    'id': 'reg_password1'
                                }))
    password2 = forms.CharField(label='请再输入密码',
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'password again',
                                    'id': 'reg_password2'
                                }))


class LogUserForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'username or email',
                                   'id': 'login_username'
                               }))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'password',
                                   'id': 'login_password'
                               }))


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
            CompetitionCnt += 1
        else:
            SlideList.append(LectureList[LectureCnt])
            LectureCnt += 1
    print(LectureCnt)
    print(CompetitionCnt)

    login = LogUserForm()
    reg = RegUserForm()

    return render(request, 'index.html',
                  {'SlideList': SlideList,
                   'CompetitionList': CompetitionList,
                   'LectureList': LectureList,
                   'login': login,
                   'reg': reg})


def competition(request, id):
    competition = Competition.objects.get(id=str(id))
    return render(request, 'single.html', {'competition': competition})


def lecture(request, id):
    lecture = Lecture.objects.get(id=str(id))
    return render(request, 'single.html', {'competition': lecture})


def competitionList(request, page):
    listLen = 4
    page = int(page)
    competitionList = Competition.objects.all()
    pagecount = (len(competitionList) - 1) // listLen + 1
    if page <= 0 or page > pagecount:
        return HttpResponse('Error!')
    if pagecount > listLen:
        competitionList = competitionList[
            (page - 1) * listLen: page * listLen]
    TagList = Tag.objects.all()
    return render(request, 'complist.html',
                  {'list': competitionList,
                   'taglist': TagList,
                   'pagelist': range(1, pagecount + 1),
                   'page': page,
                   'total': len(competitionList)})


def lectureList(request, page):
    listLen = 4
    page = int(page)
    lectureList = Lecture.objects.all()
    pagecount = (len(lectureList) - 1) // listLen + 1
    if page <= 0 or page > pagecount:
        return HttpResponse('Error!')
    if pagecount > listLen:
        lectureList = lectureList[
            (page - 1) * listLen: page * listLen]
    TagList = Tag.objects.all()
    return render(request, 'complist.html',
                  {'list': lectureList,
                   'taglist': TagList,
                   'pagelist': range(1, pagecount + 1),
                   'page': page,
                   'total': len(lectureList)})


def search_tag(request, tag):
    try:
        CompetitionList = Competition.objects.filter(tag__name=tag)
    except Competition.DoesNotExist:
        raise Http404
    try:
        LectureList = Lecture.objects.filter(tag__name=tag)
    except Lecture.DoesNotExist:
        raise Http404
    listLen = 4
    result_list = []
    CompetitionCnt = 0
    LectureCnt = 0
    for cnt in range(listLen):
        if (CompetitionCnt >= len(CompetitionList)) and (LectureCnt >= len(LectureList)):
            break
        if (CompetitionCnt >= len(CompetitionList)):
            result_list.append(LectureList[LectureCnt])
            LectureCnt += 1
            continue
        if (LectureCnt >= len(LectureList)):
            result_list.append(CompetitionList[CompetitionCnt])
            CompetitionCnt += 1
            continue
        if (CompetitionList[CompetitionCnt].date_time > LectureList[LectureCnt].date_time):
            result_list.append(CompetitionList[CompetitionCnt])
            CompetitionCnt += 1
        else:
            result_list.append(LectureList[LectureCnt])
            LectureCnt += 1
    TagList = Tag.objects.all()
    return render(request, 'complist.html', {'result_list': result_list, 'Tag': TagList})


def search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request, 'home.html')
        else:
            CompetitionList = Competition.objects.filter(title__icontains=s) | Competition.objects.filter(subtitle__icontains=s) | \
                Competition.objects.filter(intro__icontains=s) | Competition.objects.filter(content__icontains=s) | \
                Competition.objects.filter(holder__icontains=s)
            LectureList = Lecture.objects.filter(title__icontains=s) | Lecture.objects.filter(subtitle__icontains=s) | \
                Lecture.objects.filter(intro__icontains=s) | Lecture.objects.filter(content__icontains=s) | \
                Lecture.objects.filter(holder__icontains=s)
            CompetitionList.distinct()
            LectureList.distinct()
            listLen = 4
            result_list = []
            CompetitionCnt = 0
            LectureCnt = 0
            for cnt in range(listLen):
                if (CompetitionCnt >= len(CompetitionList)) and (LectureCnt >= len(LectureList)):
                    break
                if (CompetitionCnt >= len(CompetitionList)):
                    result_list.append(LectureList[LectureCnt])
                    LectureCnt += 1
                    continue
                if (LectureCnt >= len(LectureList)):
                    result_list.append(CompetitionList[CompetitionCnt])
                    CompetitionCnt += 1
                    continue
                if (CompetitionList[CompetitionCnt].date_time > LectureList[LectureCnt].date_time):
                    result_list.append(CompetitionList[CompetitionCnt])
                    CompetitionCnt += 1
                else:
                    result_list.append(LectureList[LectureCnt])
                    LectureCnt += 1
            TagList = Tag.objects.all()
            return render(request, 'complist.html', {'result_list': result_list, 'Tag': TagList})
    return HttpResponseRedirect('/')


def login(request):
    if request.method == 'POST':
        uf = LogUserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            if 'user_id' in request.session:
                return HttpResponse("You've logged in, please do not loggin twice.")
            userPassJudge = User.objects.filter(
                username__exact=username, password__exact=password)
            print(username)
            print(password)
            if userPassJudge:
                response = HttpResponse('Success')
                response.set_cookie('cookie_username', username, 3600)
                request.session['user_id'] = username
                return response
            else:
                return HttpResponse('No username or valid one')
    return HttpResponse('Not valid')


def register(request):
    Method = request.method
    if Method == 'POST':
        uf = RegUserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password1 = uf.cleaned_data['password1']
            password2 = uf.cleaned_data['password2']
            if(len(password1) != 32):
                return HttpResponse('Not valid')
            try:
                registJudge = User.objects.filter(
                    username=username).get().username
                return HttpResponse('User existed')
            except:
                registAdd = User.objects.create(
                    username=username, password=password1)
                if registAdd:
                    return HttpResponse('Success')
    return HttpResponse('Not valid')
# test login and logout

def userInfoSearch(request):
    if 'user_id' not in request.session:
        return HttpResponse("Error! Please login before you search for personal info.")
    else:
        userinfo = User.objects.get(username=request.session['user_id'])
        return render(request,'userinfo.html',{'userinfo':userinfo})

def userInfoAlter(request):
    if 'user_id' not in request.session:
        return HttpResponse("Error! Please login before you alter your personal info.")
    else:
        Method = request.method
        userinfo = User.objects.get(username=request.session['user_id'])
        print('success')
        if Method == 'POST':
            userinfo.email = request.POST.get('email')
            userinfo.stuNo = request.POST.get('stuNo')
            userinfo.stuName = request.POST.get('stuName')
            userinfo.infoUser = request.POST.get('infoUser')
            userinfo.infoPasswd = request.POST.get('infoPasswd')
            userinfo.grade = request.POST.get('grade')
            userinfo.save()
            previousInterest = userinfo.interestTag.all()
            for i in previousInterest:
                userinfo.interestTag.remove(i)
            for i in request.POST.getlist('interestTag'):
                find_i = Tag.objects.filter(name=i)
                if len(find_i) == 0:
                    p = Tag(name=i)
                    p.save()
                else:
                    p = find_i[0]
                userinfo.interestTag.add(p)
            userinfo.save()
            return HttpResponse("Your information has been saved.")
        else:
            return render_to_response('inforenew.html',{'userinfo':userinfo})
            
def index(request):
    username = request.COOKIES.get('cookie_username', '')
    return render_to_response('index4test.html', {'username': username})


def logout(request):
    response = HttpResponse(
        'logout!<br><a href="127.0.0.1:8000/regist>register</a>"')
    response.delete_cookie('cookie_username')
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return response


def slide(request):
    pass

"""
@csrf_exempt
def wechat(request):
    app = WxApp()
    result = app.process(request.GET, request.body)
    return HttpResponse(result)
"""
