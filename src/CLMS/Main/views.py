from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from Main.models import *
from django.http import Http404, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django import forms
from datetime import datetime
from Main.recommend import recommend_list
import hashlib

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
    
class idenForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'username or email',
                                   'id': 'idenForm_username'
                               }))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'password',
                                   'id': 'idenForm_password'
                               }))

def home(request):
    CompetitionList = Competition.objects.all()
    if len(CompetitionList) > 5:
        CompetitionList = CompetitionList[0:5]
    LectureList = Lecture.objects.all()
    if len(LectureList) > 5:
        LectureList = LectureList[0:5]
    for i in range(len(CompetitionList)):
        h_time = CompetitionList[i].hold_time.replace(tzinfo=None)
        print(h_time)
        if h_time > datetime.now():
            CompetitionList[i].finished = False
        else:
            CompetitionList[i].finished = True
        print(CompetitionList[i].finished)
    for i in range(len(LectureList)):
        h_time = LectureList[i].hold_time.replace(tzinfo=None)
        if h_time > datetime.now():
            LectureList[i].finished = False
        else:
            LectureList[i].finished = True
    CompetitionCnt = 0
    LectureCnt = 0
    SlideList = list()
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
    liked = False
    try:
        user = User.objects.get(username=request.session['user_id'])
        exist = user.CompetitionList.filter(id=str(id))
        liked = len(exist) > 0
    except:
        pass
    return render(request, 'competition.html', {
        'item': competition,
        'type': 'competition',
        'liked': liked
    })


def lecture(request, id):
    lecture = Lecture.objects.get(id=str(id))
    lecture.views += 1
    lecture.save()
    liked = False
    try:
        user = User.objects.get(username=request.session['user_id'])
        exist = user.LectureList.filter(id=str(id))
        liked = len(exist) > 0
    except:
        pass
    return render(request, 'lecture.html', {
        'item': lecture,
        'type': 'lecture',
        'liked': liked
    })


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
    return render(request, 'nosearchList.html',
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
    return render(request, 'nosearchList.html',
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
    return render(request, 'nosearchList.html',
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
    if not result_list or len(result_list) == 0:
        return HttpResponseRedirect('/#recom')
    if len(result_list) <= listLen * (page - 1):
        page = 1
    result_list = result_list[listLen * (page - 1):]
    TagList = Tag.objects.all()
    print(totalLen)
    return render(request, 'nosearchList.html',
                  {'list': result_list,
                   'taglist': TagList,
                   'pagelist': range(1, (totalLen - 1) // listLen + 2),
                   'page': page,
                   'total': totalLen})


def search(request):
    try:
        s = request.GET['s']
    except MultiValueDictKeyError:
        return HttpResponseRedirect('/')
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
                   'total': total,
                   's':s})


def login(request):
    if request.method == 'POST':
        uf = LogUserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            if 'user_id' in request.session:
                # HTTP response: have login before
                return HttpResponse("You've logged in, please do not loggin twice.")
            userPassJudge = User.objects.filter(
                username__exact=username, password__exact=password)
            print(username)
            print(password)
            if userPassJudge:
                # HTTP response: success log in.
                response = HttpResponse('Success')
                response.set_cookie('cookie_username', username, 3600)
                request.session['user_id'] = username
                #request.session['login_time'] = time.time()
                request.session.set_expiry(1500)
                return response
            else:
                # HTTP response: invalid username.
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
                # HTTP respose: not valid password
                return HttpResponse('Not valid')
            try:
                registJudge = User.objects.filter(
                    username=username).get().username
                # HTTP response: username existed
                return HttpResponse('User existed')
            except:
                registAdd = User.objects.create(
                    username=username, password=password1)
                if registAdd:
                    # HTTP response: register success
                    return HttpResponse('Success')
    return HttpResponse('Not valid')
# test login and logout


def userInfoSearch(request):
    if 'user_id' not in request.session:
        # HTTP response: need login auth.
        return HttpResponse("Error! Please login before you search for personal info.")
    else:
        # if time.time()-request.session['login_time']>3600:
        #    logout(request)
        #    return HttpResponse("Please login again.")                                              # HTTP response: session-id invalid.
        #request.session['login_time'] = time.time()
        userinfo = User.objects.get(username=request.session['user_id'])
        tagList = Tag.objects.all()
        #print(userinfo.usericon == '')
        # if userinfo.usericon == '':
        #    userinfo.usericon = os.getcwd()+"/static/images/leader_HWF.jpeg"                        # need to fix bug here
        #    print( userinfo.usericon)
        return render(request, 'personInfo.html', {
            'user': userinfo,
            'tagList': tagList
        })


def userInfoAlter(request):
    if request.method != 'POST':
        return JsonResponse({
            'state': -1,
            'message': 'Unsupported method'
        })
    if 'user_id' not in request.session:
        return JsonResponse({
            'state': -3,
            'message': 'Please login before action.'
        })
    try:
        user = User.objects.get(username=request.session['user_id'])
    except User.DoesNotExist:
        return JsonResponse({
            'state': -3,
            'message': 'Please login first'
        })
    try:
        if 'email' in request.POST:
            user.email = request.POST.get('email')
        if 'stuNo' in request.POST:
            user.stuNo = request.POST.get('stuNo')
        if 'stuName' in request.POST:
            user.stuName = request.POST.get('stuName')
        if 'infoUser' in request.POST:
            user.infoUser = request.POST.get('infoUser')
        if 'infoPasswd' in request.POST:
            user.infoPasswd = request.POST.get('infoPasswd')
        if 'grade' in request.POST:
            user.grade = request.POST.get('grade')
        user.save()
    except Exception as e:
        print(e)
        return JsonResponse({
            'state': -4,
            'message': 'Error!'
        })
    return JsonResponse({'state': 0})

# add new contest


def contestAdd(request):
    if 'user_id' not in request.session:
        # HTTP response: need login auth.
        return HttpResponse("Error! Please login before you add a contest.")
    else:
        # if time.time()-request.session['login_time']>3600:
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
                # HTTP response: error info adding as follows
                return HttpResponse("contest NAME CANNOT BE NULL!")
            if contestInfo.hold_time == '':
                return HttpResponse("contest HOLD TIME CANNOT BE NULL!")
            if contestInfo.holder == '':
                return HttpResponse("contest HOLDER TIME CANNOT BE NULL!")
            if contestInfo.intro == '':
                return HttpResponse("contest INTRO TIME CANNOT BE NULL!")
            if contestInfo.image == '':
                return HttpResponse("contest image TIME CANNOT BE NULL!")
            # if contestInfo.thumb == '':
            #    return HttpResponse("contest thumb TIME CANNOT BE NULL!")
            conCheck = Lecture.objects.filter(title=contestInfo.title,
                                              hold_time=contestInfo.hold_time
                                              )
            if len(conCheck) > 0:
                # HTTP response: lecture already have
                return HttpResponse("Lecture Already exists.")
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
        # HTTP response: need login auth.
        return HttpResponse("Error! Please login before you add a contest.")
    else:
        # if time.time()-request.session['login_time']>3600:
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
            # if lectureInfo.thumb == '':
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
        # HTTP response: need login auth.
        return HttpResponse("Error! Please login before you add a contest.")
    # else:
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
        # HTTP response: need login auth.
        return HttpResponse("Error! Please login before you add a contest.")
    # if time.time()-request.session['login_time']>3600:
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
        thumb_path = os.path.join(
            './media/Lecture/thumbs/', os.path.basename(str(request.FILES.get('image'))))
        thumb = make_thumb(request.FILES.get('image'), thumb_path)

        # thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_path = os.path.join(
            './Lecture/thumbs/', os.path.basename(str(request.FILES.get('image'))))
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
        lecture = Lecture.objects.get(
            id=lectureId, adminUser=request.session['user_id'])
        lecture.image = request.FILES.get('image')
        lecture.save()
        return HttpResponse("Success.")


def competitionManagement(request, conId):
    if 'user_id' not in request.session:
        # HTTP response: need login auth.
        return HttpResponse("Error! Please login before you add a contest.")
    # if time.time()-request.session['login_time']>3600:
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
            # image=request.FILES.get('image'),
            # thumb=self.thumb
        )
        # To do: many to many tag
        complist = Competition.objects.get(
            id=conId, adminUser=request.session['user_id'])
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


def like(request):
    if request.method != 'GET':
        return JsonResponse({
            'state': -1,
            'message': 'Unsupport method'
        })
    if not ('type' in request.GET and
            'id' in request.GET and
            'action' in request.GET):
        return JsonResponse({
            'state': -2,
            'message': 'Not enough params'
        })
    if 'user_id' not in request.session:
        return JsonResponse({
            'state': -3,
            'message': 'Please login first'
        })
    try:
        user = User.objects.get(username=request.session['user_id'])
    except User.DoesNotExist:
        return JsonResponse({
            'state': -3,
            'message': 'Please login first'
        })
    if request.GET['type'] == 'competition':
        exist = user.CompetitionList.filter(id=str(request.GET['id']))
        itemlist = user.CompetitionList
        try:
            item = Competition.objects.get(id=str(request.GET['id']))
        except Competition.DoesNotExist:
            return JsonResponse({
                'state': -4,
                'message': 'Competition Does Not Exist.'
            })
    elif request.GET['type'] == 'lecture':
        exist = user.LectureList.filter(id=str(request.GET['id']))
        itemlist = user.LectureList
        try:
            item = Lecture.objects.get(id=str(request.GET['id']))
        except Lecture.DoesNotExist:
            return JsonResponse({
                'state': -4,
                'message': 'Lecture Does Not Exist.'
            })
    else:
        return JsonResponse({
            'state': -5,
            'message': 'Action error!'
        })

    if len(exist) <= 0 and request.GET['action'] == 'like':
        curr = True
        item.likes += 1
        item.save()
        itemlist.add(item)
        user.save()
    elif len(exist) > 0 and request.GET['action'] == 'unlike':
        curr = False
        item.likes -= 1
        item.save()
        itemlist.remove(item)
        user.save()
    else:
        return JsonResponse({
            'state': -5,
            'message': 'Action error!'
        })
    return JsonResponse({
        'state': 0,
        'curr': curr
    })


def tag_api(request):
    if request.method != 'GET':
        return JsonResponse({
            'state': -1,
            'message': 'Unsupported method'
        })
    if not ('tag' in request.GET and
            'action' in request.GET):
        return JsonResponse({
            'state': -2,
            'message': 'Not enough params'
        })
    if 'user_id' not in request.session:
        return JsonResponse({
            'state': -3,
            'message': 'Please login first'
        })
    try:
        user = User.objects.get(username=request.session['user_id'])
    except User.DoesNotExist:
        return JsonResponse({
            'state': -3,
            'message': 'Please login first'
        })
    if request.GET['action'] == 'add':
        try:
            user.interestTag.add(request.GET['tag'])
            user.save()
        except Exception as e:
            print(e)
            return JsonResponse({
                'state': -4,
                'message': 'Error!'
            })
        return JsonResponse({'state': 0})
    elif request.GET['action'] == 'remove':
        try:
            tag = Tag.objects.get(name=request.GET['tag'])
            user.interestTag.remove(tag.id)
            user.save()
        except Exception as e:
            print(e)
            return JsonResponse({
                'state': -4,
                'message': 'Error!'
            })
        return JsonResponse({'state': 0})
    else:
        return JsonResponse({
            'state': -5,
            'message': 'Unsupported action'
        })


###if there is any bug here, call me.
def linkMainUser(request,id):    #with openid, username and password in request.
    uf = idenForm()
    if request.method != 'POST':
        request.method='POST'
    print(id)
    print(type(id))
    request.session['id']=id
    print(request.POST)
    if request.method == 'POST':
        uf = idenForm(request.POST)
        print('PSTPSPT',request.POST)
        if 'username' in request.POST:#uf.is_valid():
            username = request.POST.get('username')
            idenCode = request.session['id']
            password = hashlib.md5(request.POST.get('password').encode('utf-8')).hexdigest()# uf.cleaned_data['password']
            iden = identifyCode.objects.filter(idenCode__exact=idenCode)
            #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            print(len(iden))
            if len(iden) < 1:
                return HttpResponse("This webpage has been invalid....")
            else:
                userPassJudge = User.objects.filter(username__exact=username, password__exact=password)
                if len(userPassJudge) < 1:
                    return HttpResponse("Incorrect password or username.")
                # return HttpResponse("Success")
                return linkUser(idenCode,username,password)
                '''userPassJudge = User.objects.filter(username__exact=username, password__exact=password)
                if len(userPassJudge) < 1:
                    return HttpResponse("Incorrect password or username.")
                return HttpResponse("Success")'''

    else:
        return HttpResponse("error here. Invalid message type")
    return render(request,'wechatLink.html',{'uf':uf})
    

    
def linkUser(idenCode,username,password):
    userPassJudge = User.objects.filter(
        username__exact=username, password__exact=password)
    if len(userPassJudge) == 0:
        return HttpResponse("Invalid username or password.")    
    else:
        user = userPassJudge[0]
        openid = identifyCode.objects.filter(idenCode__exact=idenCode)
        openid = openid[0].openid
        openid_check = wechatUser.objects.filter(openid=openid,userLink=True)
        if len(openid_check):
            return HttpResponse("You've already linked one before. Please unlink your present wechat account.") 
        wechatUser.objects.create(openid=openid)
        openid_check = wechatUser.objects.filter(openid=openid)  
        wechat_user = openid_check[0]
        wechat_user.mainUser = user             #link user
        wechat_user.userLink = True             #set flag as linked.
        wechat_user.save()
        identifyCode.objects.filter(idenCode__exact=idenCode).delete()
    return HttpResponse("Success.")    

