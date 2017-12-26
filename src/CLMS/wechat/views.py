from __future__ import unicode_literals
from Main.models import *
from Main.views import LogUserForm,linkMainUser
# Create your views here.
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, \
    VideoMessage, LinkMessage, LocationMessage, EventMessage
from secret import Secret
import hashlib
import os
import numpy

### wechat open_id to user_id has been linked. 
### if the user has linked before, we can use the following two statements to find whatever things in user.
''' openid_check = wechatUser.objects.filter(openid=openid,userLink=True)
    if openid_check:
        user = openid_check[0].mainUser
    else:
        return Failure.'''
### to fetch whatever things in User type 'user'      
### and what you only need to change is openid.    :-)                Luka.

wechat_instance = WechatBasic(
    token=Secret.SECRET_TOKEN,
    appid=Secret.APP_ID,
    appsecret=Secret.ENCODING_AES_KEY)
home_url = Secret.HOME_URL


@csrf_exempt
def wechat(request):
    if request.method == 'GET':  # verifycation
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HTTPResponseBadRequest('Verify Failed')
        return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")

    # parse the XML
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    message = wechat_instance.get_message()
    user_info = wechat_instance.get_user_info(message.source)

    if isinstance(message, TextMessage):
        content = message.content.strip()
        if content == 'Competition' or content == '竞赛':
            return HttpResponse(wechat_instance.response_news(get_new_comps(request)), content_type="application/xml")
        elif content == 'Lecture' or content == '讲座':
            return HttpResponse(wechat_instance.response_news(get_new_lecs(request)), content_type="application/xml")
        elif content == 'Tags' or content == '订阅标签':
            TagList = Tag.objects.all()
            reply_text = ''
            for tag in TagList:
                reply_text += '回复“tag:' + tag.name + '“查看该标签下最新动态\n'
            if not reply_text:
                reply_text += ':(sorry,no tag'
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
        elif content[:3] == 'tag':
            tag = content[4:]
            if not tag:
                reply_text = "请输入一个tag"
                response = wechat_instance.response_text(content=reply_text)
                return HttpResponse(response, content_type="application/xml")
            else:
                return HttpResponse(wechat_instance.response_news(tagProcess(tag)), content_type="application/xml")
        # wechat 查看基于订阅的推荐   
        elif content == '查看':
            open_id = user_info['openid']
            return recommend(open_id=open_id)
            
        # wechat 订阅
        elif content[:3] == 'add':
            tag = content[4:]
            open_id = user_info['openid']
            if not tag:
                reply_text = "请输入一个tag"
            else:
                reply_text = add_interest(open_id=open_id, tag=tag)
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
        elif content == '添加':
            reply_text = '回复‘add:’和以下任意个标签订阅该标签相关信息\n'
            TagList = Tag.objects.all()
            for tag in TagList:
                reply_text += tag.name + '\n'
            if not TagList:
                reply_text = ':(Sorry,no tag'
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
        elif content == 'link':
            open_id = user_info['openid']
            if checkWechatUser(open_id):
                reply_text = "already registed"
            else:
                return pageLink(open_id=open_id) 
        elif content == 'unlink':
            open_id = user_info['openid']
            if unlinkMainUser(open_id):
                reply_text = ('Unlinked successfully.')
            else:
                reply_text = ('well, you might have not linked before :-)')
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
        elif content == 'function' or '功能':
            reply_text = ('回复Competition或‘竞赛’查看最新竞赛信息\n' + '回复Tags或‘订阅标签’查看可订阅标签信息\n'
                          '回复Lecture或‘讲座’查看最新讲座信息\n' + '回复‘添加’添加微信订阅\n' + 
                          '回复‘查看’查看微信订阅')
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
        else:
            reply_text = ('当前无匹配，请重试\n' + '回复Competition或‘竞赛’查看最新竞赛信息\n' + '回复Tags或‘订阅标签’查看可订阅标签信息\n'
                          '回复Lecture或‘讲座’查看最新讲座信息\n' + '回复‘添加’添加微信订阅\n' + 
                          '回复‘查看’查看微信订阅')
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
    else:
        if isinstance(message, EventMessage):
            if message.type == 'subscribe':  ###
                reply_text = '感谢您的到来!回复“功能”返回使用指南'
                open_id = user_info['openid']
                # open_checkWechatUserid = user_info['openid']
                #isRegist = wechat_new_user(open_id)
                #changed on Dec.22nd                     Luka.
                isRegist = checkWechatUser(open_id)
                if isRegist:
                    reply_text += 'Welcome ' + isRegist.mainUser.username +'return \'unlink \' to unlink your present account.'
                else:
                    # wechat_new_user(open_id=open_id)
                    reply_text += 'return \'link \' to link your wechat account to the main database..'
            else:
                reply_text = ('功能尚未实现')
        else:
            reply_text = ('无匹配功能')

        response = wechat_instance.response_text(content=reply_text)
        return HttpResponse(response, content_type="application/xml")


def get_new_comps(request):
    listLen = 4
    competition_list = Competition.objects.all()
    if len(competition_list) > listLen:
        competitionList = competition_list[0:listLen - 1]
    return comp_to_array(competition_list)


def comp_to_array(comp_list):
    response = []
    for comp in comp_list:
        response.append({
            'title': comp.title,
            'picurl': os.path.join(home_url, comp.thumb.url),
            'description': comp.intro,
            'url': home_url + '/' + 'competition' + '/' + str(comp.id) + '/'
        })
    if not response:
        response.append({
            'title': "home",
            'picurl': "",
            'description': "home",
            'url': home_url
        })
    return response


def get_new_lecs(request):
    listLen = 4
    lectureList = Lecture.objects.all()
    if len(lectureList) > listLen:
        lectureList = lectureList[0:listLen - 1]
    return lec_to_array(lectureList)


def lec_to_array(lecs_list):
    response = []
    for lec in lecs_list:
        response.append({
            'title': lec.title,
            'picurl': os.path.join(home_url, lec.thumb.url),
            'description': lec.intro,
            'url': home_url + '/' + 'lecture' + '/' + str(lec.id) + '/'
        })
    if not response:
        response.append({
            'title': "home",
            'picurl': "",
            'description': "home",
            'url': home_url
        })
    return response


def tagProcess(tag):
    try:
        CompetitionList = Competition.objects.filter(tag__name=tag)
    except Competition.DoesNotExist:
        pass
    try:
        LectureList = Lecture.objects.filter(tag__name=tag)
    except Lecture.DoesNotExist:
        pass
    listLen = 2
    response = []
    if len(CompetitionList) <= listLen:
        for comp in CompetitionList:
            response.append({
                'title' : comp.title,
                'picurl' : os.path.join(home_url, comp.thumb.url),
                'description' : comp.intro,
                'url' : home_url + '/' + 'competition' + '/' + str(comp.id) + '/'
            })
    else:
        for comp in CompetitionList[:listLen]:
            response.append({
                'title' : comp.title,
                'picurl' : os.path.join(home_url, comp.thumb.url),
                'description' : comp.intro,
                'url' : home_url + '/' + 'competition' + '/' + str(comp.id) + '/'
            })
    if  len(LectureList) <= listLen:
        for lec in LectureList:
            response.append({
                'title' : lec.title,
                'picurl' : os.path.join(home_url, lec.thumb.url),
                'description' : lec.intro,
                'url' : home_url + '/' + 'competition' + '/' + str(lec.id) + '/'
                })
    else:
        for lec in LectureList[:listLen]:
            response.append({
                'title' : lec.title,
                'picurl' : os.path.join(home_url, lec.thumb.url),
                'description' : lec.intro,
                'url' : home_url + '/' + 'competition' + '/' + str(lec.id) + '/'
                })
    if not response:
        response.append({
            'title': "home",
            'picurl': "",
            'description': "home",
            'url': home_url
        })
    return response
    # return HttpResponse(wechat_instance.response_news(response), content_type="application/xml")


def wechat_new_user(open_id):
    registAdd = User.objects.create(
                    username=open_id)
    if registAdd:
        return True
    return False


def add_interest(open_id, tag):
    openid_check = wechatUser.objects.filter(openid=open_id,userLink=True)
    if openid_check:
        user = openid_check[0].mainUser
    else:
        return 'please link with main database first\n' + 'return \'link \' to link your wechat account to the main database..'
    find_tag = Tag.objects.filter(name__exact=tag)
    if len(find_tag) == 0:
        p = Tag(name=tag)
        p.save()
    else:
        p = find_tag[0]
    user.interestTag.add(p)
    user.save()
    return 'successful'


def recommend(open_id):
    reply_text = 'please link with main database first\n' + 'return \'link \' to link your wechat account to the main database..'
    CompetitionList_by_interest = Competition.objects.filter(tag__name='a tag you will never use')
    LectureList_by_interest = Lecture.objects.filter(tag__name='a tag you will never use')
    response = []
    openid_check = wechatUser.objects.filter(openid=open_id,userLink=True)
    if openid_check:
        user = openid_check[0].mainUser
    else:
        response = wechat_instance.response_text(content=reply_text)
        return HttpResponse(response, content_type="application/xml")
    for tag in user.interestTag.all():              # 按interestTag搜
        response += tagProcess(tag=tag)
    if len(response) >= 5:
        response = response[:5]
    if not response:
        response.append({
            'title': "home",
            'picurl': "",
            'description': "home",
            'url': home_url
        })
    return HttpResponse(wechat_instance.response_news(response), content_type="application/xml")

### wechat information add on Dec.22nd    
# First, wechat user login and check if its in database and whether have linked to a main_user
# Second, if openid exists and linked, user openid as a pointer
# else, as the user to link it through a website or sth....
# Luka.

# Function to check whether wechat open_id in database
def checkWechatUser(openid):
    openid_check = wechatUser.objects.filter(openid=openid,userLink=True)
    if openid_check:
        return True
    else:
        return False
    
# Function to check whether openid has linked to a correct userid when linking

# Function to unlink
def unlinkMainUser(openid):
    openid_check = wechatUser.objects.filter(openid=openid,userLink=True)
    if openid_check:
        wechat_user = openid_check[0]
        wechat_user.userLink = False
        wechat_user.save()
        return True
    return False

def generateRandomIden(openid):
    randomInt = ''
    for _ in range(15):
        randomInt += str(numpy.random.randint(0,10))
    Identity = identifyCode()
    Identity.idenCode = randomInt
    Identity.openid = openid
    Identity.save()
    return randomInt


def pageLink(open_id):
    identity = generateRandomIden(open_id)
    webpage = home_url+'/wechatLink/'+str(identity)
    #webpage = home_url + '/wechatLink/' + 'openid=' + open_id
    response = []
    response.append({
        'title': "linkPage",
        'picurl': "",
        'description': "linkPage",
        'url': webpage
        })
    return HttpResponse(wechat_instance.response_news(response), content_type="application/xml")
#TODO: Finish this page as well as functions.
# we need an empty html.......
# def pageLink(openid,request):
#     identity = generateRandomIden(openid)
#     webpage = home_url+'/wechatLink'
#     reply_text = ('your identity code is '+identity+'. Please link it through the following website'+webpage)  
#     return reply_text
    #bugs may appears here... 
    # Just suppose I can have one and can direct the link to localhost/wechatLink with request contains openid :-)  Luka
    # return render(request,'wechatLink.html',{'uf':uf})
