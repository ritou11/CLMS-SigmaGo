from django.shortcuts import render
from django.http import HttpResponse
from Main.models import Competition, Lecture
from datetime import datetime
from django.http import Http404
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

    return render(request, 'home.html', {'SlideList':SlideList,'CompetitionList': CompetitionList, 'LectureList': LectureList})


def competition(request, id):
    pass


def lecture(request, id):
    pass


def competitionList(request):
    pass


def lectureList(request):
    pass


def login(request):
    pass


def register(request):
    pass

def slide(request):
    pass