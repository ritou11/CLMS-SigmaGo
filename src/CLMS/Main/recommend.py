from Main.models import User, Competition, Lecture


def recommend_list(request, maxlen):
    try:
        user = User.objects.get(username=request.session['user_id'])
    except User.DoesNotExist:
        return None, 0
    CompetitionList = Competition.objects.filter(
        tag__name='a tag you will never use')
    LectureList = Lecture.objects.filter(tag__name='a tag you will never use')
    for tag in user.interestTag.all():
        try:
            CompetitionList = CompetitionList | Competition.objects.filter(
                tag__name=str(tag))
        except Competition.DoesNotExist:
            pass
        try:
            LectureList = LectureList | Lecture.objects.filter(tag__name=(tag))
        except Lecture.DoesNotExist:
            pass
    CompetitionList.distinct()
    LectureList.distinct()
    result_list = list()
    CompetitionCnt = 0
    LectureCnt = 0
    for cnt in range(maxlen):
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
    return result_list, len(CompetitionList) + len(LectureList)
