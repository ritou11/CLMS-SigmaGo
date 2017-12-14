from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from Main.models import *
from datetime import datetime
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datastructures import MultiValueDictKeyError
from django import forms
from django.db import models
from PIL import Image
import hashlib
import time
import datetime
from Main.recommend import recommend_list
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
        CompetitionList = CompetitionList[0:5]
    LectureList = Lecture.objects.all()
    if len(LectureList) > 5:
        LectureList = LectureList[0:5]
    for i in range(len(CompetitionList)):
        if CompetitionList[i].hold_time > CompetitionList[i].date_time:
            CompetitionList[i].finished = False
        else:
            CompetitionList[i].finished = True
        print(CompetitionList[i].finished)
    for i in range(len(LectureList)):
        if LectureList[i].hold_time > datetime[i].date_time:
            LectureList[i].finished = False
        else:
            LectureList[i].finished = True
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

    logged = True
    try:
        userinfo = User.objects.get(username=request.session['user_id'])
    except (User.DoesNotExist, KeyError):
        logged = False

    if logged:
        recommendList, recommendLen = recommend_list(request, 3)
        if not recommendList:
            recommendList = SlideList
    else:
        recommendList = SlideList

    login = LogUserForm()
    reg = RegUserForm()

    render_dict = {'SlideList': recommendList,
                   'CompetitionList': CompetitionList,
                   'LectureList': LectureList,
                   # 'RecommendList': recommendList,
                   'login': login,
                   'reg': reg,
                   'logged': logged}
    if logged:
        render_dict['user'] = userinfo
    return render(request, 'index.html', render_dict)


def competition(request, id):
    competition = Competition.objects.get(id=str(id))
    competition.views += 1
    competition.save()
    return render(request, 'single.html', {'item': competition})


def lecture(request, id):
    lecture = Lecture.objects.get(id=str(id))
    lecture.views += 1
    lecture.save()
    return render(request, 'single.html', {'item': lecture})


def competitionList(request, page):
    listLen = 4
    try:
        page = int(page)
    except ValueError:
        page = 1
    competitionList = Competition.objects.all()
    total = len(competitionList)
    pagecount = (len(competitionList) - 1) // listLen + 1
    if page <= 0 or page > pagecount:
        return HttpResponse('Error!')
    if len(competitionList) > listLen:
        competitionList = competitionList[
            (page - 1) * listLen: min(len(competitionList), page * listLen)]
    TagList = Tag.objects.all()
    return render(request, 'List.html',
                  {'list': competitionList,
                   'taglist': TagList,
                   'pagelist': range(1, pagecount + 1),
                   'page': page,
                   'total': total})


def lectureList(request, page):
    listLen = 4
    try:
        page = int(page)
    except ValueError:
        page = 1
    lectureList = Lecture.objects.all()
    total = len(lectureList)
    pagecount = (len(lectureList) - 1) // listLen + 1
    if page <= 0 or page > pagecount:
        return HttpResponse('Error!')
    if len(lectureList) > listLen:
        lectureList = lectureList[
            (page - 1) * listLen: min(len(lectureList), page * listLen)]
    TagList = Tag.objects.all()
    return render(request, 'List.html',
                  {'list': lectureList,
                   'taglist': TagList,
                   'pagelist': range(1, pagecount + 1),
                   'page': page,
                   'total': total})


def search_tag(request, tag, page):
    try:
        CompetitionList = Competition.objects.filter(tag__name=tag)
    except Competition.DoesNotExist:
        pass
    try:
        LectureList = Lecture.objects.filter(tag__name=tag)
    except Lecture.DoesNotExist:
        pass
    listLen = 4
    result_list = []
    CompetitionCnt = 0
    LectureCnt = 0
    try:
        page = int(page)
    except ValueError:
        page = 1

    for cnt in range(listLen * page):
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

    if len(result_list) <= listLen * (page - 1):
        raise Http404

    total = len(CompetitionList) + len(LectureList)
    result_list = result_list[listLen * (page - 1):]
    TagList = Tag.objects.all()
    return render(request, 'List.html',
                  {'list': result_list,
                   'taglist': TagList,
                   'pagelist': range(1, (len(CompetitionList) + len(LectureList) - 1) // listLen + 2),
                   'page': page,
                   'total': total})


def recommend(request, page):
    listLen = 4
    try:
        page = int(page)
    except ValueError:
        page = 1
    result_list, totalLen = recommend_list(request, listLen * page)
    if not result_list:
        raise Http404
    if len(result_list) <= listLen * (page - 1):
        raise Http404
    result_list = result_list[listLen * (page - 1):]
    TagList = Tag.objects.all()
    return render(request, 'List.html',
                  {'list': result_list,
                   'taglist': TagList,
                   'pagelist': range(1, (totalLen - 1) // listLen + 2),
                   'page': page,
                   'total': len(result_list)})


def search(request):
    if 's' in request.GET:
        try:
            s = request.GET['s']
        except MultiValueDictKeyError:
            return home(request)
        try:
            page = request.GET['page']
            page = int(page)
        except (ValueError, MultiValueDictKeyError):
            page = 1
        CompetitionList = Competition.objects.filter(title__icontains=s) | Competition.objects.filter(subtitle__icontains=s) | \
            Competition.objects.filter(intro__icontains=s) | Competition.objects.filter(content__icontains=s) | \
            Competition.objects.filter(holder__icontains=s)
        LectureList = Lecture.objects.filter(title__icontains=s) | Lecture.objects.filter(subtitle__icontains=s) | \
            Lecture.objects.filter(intro__icontains=s) | Lecture.objects.filter(content__icontains=s) | \
            Lecture.objects.filter(holder__icontains=s)
        CompetitionList.distinct()
        LectureList.distinct()
        total = len(CompetitionList) + len(LectureList)
        listLen = 4
        result_list = []
        CompetitionCnt = 0
        LectureCnt = 0
        for cnt in range(listLen * page):
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
        result_list = result_list[listLen * (page - 1):]
        TagList = Tag.objects.all()
        return render(request, 'List.html',
                      {'list': result_list,
                       'taglist': TagList,
                       'pagelist': range(1, (total - 1) // listLen + 2),
                       'page': page,
                       'total': total})


def login(request):
    if request.method == 'POST':
        uf = LogUserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            if 'user_id' in request.session:
                return HttpResponse("You've logged in, please do not loggin twice.")             # HTTP response: have login before
            userPassJudge = User.objects.filter(
                username__exact=username, password__exact=password)
            print(username)
            print(password)
            if userPassJudge:
                response = HttpResponse('Success')                                               # HTTP response: success log in.
                response.set_cookie('cookie_username', username, 3600)
                request.session['user_id'] = username
                #request.session['login_time'] = time.time()
                request.session.set_expiry(1500)
                return response
            else:
                return HttpResponse('No username or valid one')                                  # HTTP response: invalid username.
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
                return HttpResponse('Not valid')                # HTTP respose: not valid password
            try:
                registJudge = User.objects.filter(
                    username=username).get().username
                return HttpResponse('User existed')             # HTTP response: username existed
            except:
                registAdd = User.objects.create(
                    username=username, password=password1)
                if registAdd:
                    return HttpResponse('Success')              # HTTP response: register success
    return HttpResponse('Not valid')
# test login and logout


def userInfoSearch(request):
    if 'user_id' not in request.session:
        return HttpResponse("Error! Please login before you search for personal info.")             # HTTP response: need login auth.
    else:
        #if time.time()-request.session['login_time']>3600:
        #    logout(request)
        #    return HttpResponse("Please login again.")                                              # HTTP response: session-id invalid.
        #request.session['login_time'] = time.time()
        userinfo = User.objects.get(username=request.session['user_id'])
        return render(request, 'personInfo.html', {'user': userinfo})


def userInfoAlter(request):
    if 'user_id' not in request.session:
        return HttpResponse("Error! Please login before you alter your personal info.")             # HTTP response: need login auth.
    else:
        #if time.time()-request.session['login_time']>3600:
        #    logout(request)
        #    return HttpResponse("Please login again.")
        #request.session['login_time'] = time.time()
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
            #lecture = Lecture.objects.get(id=lectureId,adminUser=request.session['user_id'])
            userinfo.userImage = request.FILES.get('image')
            if not userinfo.userImage:
                return HttpResponse("Image cannot be null.")
            userinfo.save_with_photo()
            previousInterest = Tag.objects.all()
            for i in previousInterest:
                userinfo.interestTag.remove(i)
            for i in request.POST.getlist('interestTag'):
                find_i = Tag.objects.filter(name__exact=i)
                if len(find_i) == 0:
                    p = Tag(name=i)
                    p.save()
                else:
                    p = find_i[0]
                userinfo.interestTag.add(p)
            userinfo.save_with_photo()
            return HttpResponse("Your information has been saved.")                     # HTTP response: info saved successfully
        else:
            return render_to_response('inforenew.html', {'userinfo': userinfo})

# add new contest


def contestAdd(request):
    if 'user_id' not in request.session:
        return HttpResponse("Error! Please login before you add a contest.")             # HTTP response: need login auth.
    else:
        #if time.time()-request.session['login_time']>3600:
        #    logout(request)
        #    return HttpResponse("Please login again.")
        #request.session['login_time'] = time.time()
        userinfo = User.objects.get(username=request.session['user_id'])
        if userinfo.adminAuth == False:
            return HttpResponse("Sorry, but you are not admin user, please contact xxx@xxx.xxx")
        Method = request.method
        contestInfo = Competition()
        print('success')
        if Method == 'POST':
            contestInfo.title = request.POST.get('title')
            contestInfo.subtitle = request.POST.get('subtitle')
            contestInfo.hold_time = request.POST.get('hold_time')
            contestInfo.holder = request.POST.get('holder')
            contestInfo.state = request.POST.get('state')
            contestInfo.intro = request.POST.get('intro')
            contestInfo.content = request.POST.get('content')
            contestInfo.method = request.POST.get('method')
            contestInfo.award = request.POST.get('award')
            contestInfo.image = request.FILES.get('image')
            #contestInfo.thumb = request.FILES.get('thumb')
            contestInfo.adminUser = request.session['user_id']
            if contestInfo.title == '':
                return HttpResponse("contest NAME CANNOT BE NULL!")                         # HTTP response: error info adding as follows
            if contestInfo.hold_time == '':
                return HttpResponse("contest HOLD TIME CANNOT BE NULL!")
            if contestInfo.holder == '':
                return HttpResponse("contest HOLDER TIME CANNOT BE NULL!")
            if contestInfo.intro == '':
                return HttpResponse("contest INTRO TIME CANNOT BE NULL!")
            if contestInfo.image == '':
                return HttpResponse("contest image TIME CANNOT BE NULL!")
            #if contestInfo.thumb == '':
            #    return HttpResponse("contest thumb TIME CANNOT BE NULL!")
            conCheck = Lecture.objects.filter(title=contestInfo.title,
                                              hold_time=contestInfo.hold_time
                                              )
            if len(conCheck) > 0:
                return HttpResponse("Lecture Already exists.")                              # HTTP response: lecture already have
            contestInfo.save()
            for i in request.POST.getlist('interestTag'):
                find_i = Tag.objects.filter(name__exact=i)
                if len(find_i) == 0:
                    p = Tag(name=i)
                    p.save()
                else:
                    p = find_i[0]
                contestInfo.tag.add(p)
            contestInfo.save()
            return HttpResponse("Contest info has been saved.")
        else:
            contestInfo = Competition()
            return render_to_response('contestInfo.html', {'contestInfo': contestInfo})

# add new lecture


def lectureAdd(request):
    if 'user_id' not in request.session:
        return HttpResponse("Error! Please login before you add a contest.")             # HTTP response: need login auth.
    else:
        #if time.time()-request.session['login_time']>3600:
        #    logout(request)
        #    return HttpResponse("Please login again.")
        #request.session['login_time'] = time.time()
        userinfo = User.objects.get(username=request.session['user_id'])
        if userinfo.adminAuth == False:
            return HttpResponse("Sorry, but you are not admin user, please contact xxx@xxx.xxx")
        Method = request.method
        lectureInfo = Lecture()
        if Method == 'POST':
            lectureInfo.title = request.POST.get('title')
            lectureInfo.subtitle = request.POST.get('subtitle')
            lectureInfo.hold_time = request.POST.get('hold_time')
            lectureInfo.holder = request.POST.get('holder')
            lectureInfo.state = request.POST.get('state')
            lectureInfo.intro = request.POST.get('intro')
            lectureInfo.content = request.POST.get('content')
            lectureInfo.method = request.POST.get('method')
            lectureInfo.image = request.FILES.get('image')
            #lectureInfo.thumb = request.FILES.get('thumb')
            lectureInfo.adminUser = request.session['user_id']
            if lectureInfo.title == '':
                return HttpResponse("LECTURE NAME CANNOT BE NULL!")
            if lectureInfo.hold_time == '':
                return HttpResponse("LECTURE HOLD TIME CANNOT BE NULL!")
            if lectureInfo.holder == '':
                return HttpResponse("LECTURE HOLDER TIME CANNOT BE NULL!")
            if lectureInfo.intro == '':
                return HttpResponse("LECTURE INTRO TIME CANNOT BE NULL!")
            if lectureInfo.image == '':
                return HttpResponse("LECTURE image TIME CANNOT BE NULL!")
            #if lectureInfo.thumb == '':
            #    return HttpResponse("LECTURE thumb TIME CANNOT BE NULL!")
            lecCheck = Lecture.objects.filter(title=lectureInfo.title,
                                              hold_time=lectureInfo.hold_time
                                              )
            if len(lecCheck) > 0:
                return HttpResponse("Lecture Already exists.")
            lectureInfo.save()
            for i in request.POST.getlist('interestTag'):
                find_i = Tag.objects.filter(name__exact=i)
                if len(find_i) == 0:
                    p = Tag(name=i)
                    p.save()
                else:
                    p = find_i[0]
                lectureInfo.tag.add(p)
            lectureInfo.save()
            return HttpResponse("lecture info has been saved.")
        else:
            lectureInfo = Lecture()
            return render_to_response('lectureInfo.html', {'lectureInfo': lectureInfo})


def lecConManagement(request):
    if 'user_id' not in request.session:
        return HttpResponse("Error! Please login before you add a contest.")             # HTTP response: need login auth.
    #else:
    #    if time.time()-request.session['login_time']>3600:
    #        logout(request)
    #        return HttpResponse("Please login again.")
    #    request.session['login_time'] = time.time()
    userinfo = User.objects.get(username=request.session['user_id'])
    if userinfo.adminAuth == False:
        return HttpResponse("Sorry, but you are not admin user, please contact xxx@xxx.xxx")
    lectureList = Lecture.objects.filter(
        adminUser__exact=request.session['user_id'])
    contestList = Competition.objects.filter(
        adminUser__exact=request.session['user_id'])
    return render_to_response('adminManage.html', {'Competitions': contestList, 'Lectures': lectureList})


def lectureManagement(request, lectureId):
    if 'user_id' not in request.session:
        return HttpResponse("Error! Please login before you add a contest.")            # HTTP response: need login auth.
    #if time.time()-request.session['login_time']>3600:
    #    logout(request)
    #    return HttpResponse("Please login again.")
    #request.session['login_time'] = time.time()
    try:
        lecture = Lecture.objects.get(
            id=lectureId, adminUser=request.session['user_id'])
    except:
        return HttpResponse("Nothing found here.....")
    # if len(lecture) < 1:
    #    return HttpResponse("Nothing found here.....")
    if request.method != 'POST':
        return render_to_response('lectureInfoRenew.html', {'lecture': lecture})
    else:
        print(str(request.FILES.get('image')))
        thumb_path = os.path.join('./media/Lecture/thumbs/', os.path.basename(str(request.FILES.get('image'))))
        thumb = make_thumb(request.FILES.get('image'), thumb_path)

        # thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_path = os.path.join('./Lecture/thumbs/', os.path.basename(str(request.FILES.get('image'))))
        #thumb = ImageFieldFile(thumb, thumb_path)
        Lecture.objects.filter(id__exact=lectureId,
                               adminUser__exact=request.session['user_id']).update(
            title=request.POST.get('title'),
            subtitle=request.POST.get('subtitle'),
            hold_time=request.POST.get('hold_time'),
            holder=request.POST.get('holder'),
            state=request.POST.get('state'),
            intro=request.POST.get('intro'),
            content=request.POST.get('content'),
        )
        # To do: many to many tag
        lecture = Lecture.objects.get(id=lectureId,adminUser=request.session['user_id'])
        lecture.image = request.FILES.get('image')
        lecture.save()
        return HttpResponse("Success.")


def competitionManagement(request, conId):
    if 'user_id' not in request.session:
        return HttpResponse("Error! Please login before you add a contest.")             # HTTP response: need login auth.
    #if time.time()-request.session['login_time']>3600:
    #    logout(request)
    #    return HttpResponse("Please login again.")
    #request.session['login_time'] = time.time()
    try:
        contest = Competition.objects.get(
            id=conId, adminUser=request.session['user_id'])
    except:
        return HttpResponse("Nothing found here.....")
    print(contest)
    # if len(contest) < 1:
    #    return HttpResponse("Nothing found here.....")
    if request.method != 'POST':
        return render_to_response('contestInfoRenew.html', {'contest': contest})
    else:   
        thumb_path = os.path.join(
            './media/Competition/thumbs/', os.path.basename(request.FILES.get('image')))
        make_thumb(request.FILES.get('image'), thumb_path)

        # thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_path = os.path.join(
            './Competition/thumbs/', os.path.basename(request.FILES.get('image')))
        #self.thumb = ImageFieldFile(self, self.thumb, thumb_path)
        Competition.objects.filter(id__exact=conId,
                                   adminUser__exact=request.session['user_id']).update(
            title=request.POST.get('title'),
            subtitle=request.POST.get('subtitle'),
            hold_time=request.POST.get('hold_time'),
            holder=request.POST.get('holder'),
            state=request.POST.get('state'),
            intro=request.POST.get('intro'),
            award=request.POST.get('award'),
            content=request.POST.get('content'),
            method=request.POST.get('method'),
            #image=request.FILES.get('image'),
            #thumb=self.thumb
        )
        # To do: many to many tag
        complist = Competition.objects.get(id=conId,adminUser=request.session['user_id'])
        complist.image = request.FILES.get('image')
        complist.save()
        return HttpResponse("Success.")


def index(request):
    username = request.COOKIES.get('cookie_username', '')
    return render_to_response('index4test.html', {'username': username})


def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('cookie_username')
    try:
        del request.session['user_id']
        del request.session['login_time']
    except KeyError:
        pass
    return response


def likeCompetition(request, id):
    pwd = request.get_full_path().replace('competition-like', 'competition')
    try:
        competition = Competition.objects.get(id=str(id))
        competition.views -= 1
        competition.save()
    except:
        raise Http404
    try:
        user = User.objects.get(username=request.session['user_id'])
    except:
        return HttpResponseRedirect(pwd)

    exist = user.CompetitionList.filter(id=str(id))

    if len(exist) == 0:

        competition.likes += 1
        competition.save()
        user.CompetitionList.add(competition)
    else:
        competition.likes -= 1
        competition.save()
        user.CompetitionList.remove(competition)
    return HttpResponseRedirect(pwd)


def likeLecture(request, id):
    pwd = request.get_full_path().replace('lecture-like', 'lecture')
    try:
        lecture = Lecture.objects.get(id=str(id))
        lecture.views -= 1
        lecture.save()
    except:
        raise Http404
    try:
        user = User.objects.get(username=request.session['user_id'])
    except:
        return HttpResponseRedirect(pwd)

    exist = user.LectureList.filter(id=str(id))

    if len(exist) == 0:

        lecture.likes += 1
        lecture.save()
        user.LectureList.add(lecture)
    else:
        lecture.likes -= 1
        lecture.save()
        user.LectureList.remove(lecture)
    return HttpResponseRedirect(pwd)
