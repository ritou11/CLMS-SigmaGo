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
    return render(request, 'home.html', {'CompetitionList': CompetitionList, 'LectureList': LectureList})


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
