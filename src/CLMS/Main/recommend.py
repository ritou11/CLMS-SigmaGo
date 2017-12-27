from Main.models import User, Competition, Lecture


def recommend_list(request, maxlen):
    try:
        user = User.objects.get(username=request.session['user_id'])
    except :
        return None, 0

    CompetitionList_by_grade = Competition.objects.filter(tag__name='a tag you will never use')
    LectureList_by_grade = Lecture.objects.filter(tag__name='a tag you will never use')

    CompetitionList_by_interest = Competition.objects.filter(tag__name='a tag you will never use')
    LectureList_by_interest = Lecture.objects.filter(tag__name='a tag you will never use')

    CompetitionList = Competition.objects.filter(tag__name='a tag you will never use')
    LectureList = Lecture.objects.filter(tag__name='a tag you will never use')

    grd = user.grade                                # 按年级搜
    if grd == '本科一年级' or grd == '本科二年级':
        tag = 'LowGrade'
    elif grd == '本科三年级' or grd == '本科四年级' or grd == '本科五年级及以上':
        tag = 'HighGrade'
    else:
        tag = 'graduate'

    try:
        CompetitionList_by_grade = CompetitionList_by_grade | Competition.objects.filter(tag__name=tag)
    except Competition.DoesNotExist:
        pass
    try:
        LectureList_by_grade = LectureList_by_grade | Lecture.objects.filter(tag__name=tag)
    except Lecture.DoesNotExist:
        pass

    for tag in user.interestTag.all():              # 按interestTag搜
        try:
            CompetitionList_by_interest = CompetitionList_by_interest | Competition.objects.filter(
                tag__name=str(tag))
        except Competition.DoesNotExist:
            pass
        try:
            LectureList_by_interest = LectureList_by_interest | Lecture.objects.filter(tag__name=(tag))
        except Lecture.DoesNotExist:
            pass

    CompetitionList = CompetitionList_by_grade & CompetitionList_by_interest
    LectureList = LectureList_by_grade & LectureList_by_interest

    CompetitionList = CompetitionList | CompetitionList_by_grade | CompetitionList_by_interest
    LectureList = LectureList | LectureList_by_grade | LectureList_by_interest
    
    CompetitionList = CompetitionList.distinct()
    LectureList = LectureList.distinct()
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

    result_list_len = len(CompetitionList) + len(LectureList)

    if result_list_len < maxlen:
	    CompetitionList_extra = Competition.objects.all()
	    if len(CompetitionList_extra) > 5:
	        CompetitionList_extra = CompetitionList_extra[0:5]

	    LectureList_extra = Lecture.objects.all()
	    if len(LectureList_extra) > 5:
	        LectureList_extra = LectureList_extra[0:5]

	    CompetitionCnt_extra = 0
	    LectureCnt_extra = 0
	    SlideList_extra = list()
	    for cnt in range(maxlen):
	        if (CompetitionCnt_extra >= len(CompetitionList_extra)) and (LectureCnt_extra >= len(LectureList_extra)):
	            break
	        if (CompetitionCnt_extra >= len(CompetitionList_extra)):
	            SlideList_extra.append(LectureList_extra[LectureCnt_extra])
	            LectureCnt_extra += 1
	            continue
	        if (LectureCnt_extra >= len(LectureList_extra)):
	            SlideList_extra.append(CompetitionList_extra[CompetitionCnt_extra])
	            CompetitionCnt_extra += 1
	            continue
	        if (CompetitionList_extra[CompetitionCnt_extra].date_time > LectureList_extra[LectureCnt_extra].date_time):
	            SlideList_extra.append(CompetitionList_extra[CompetitionCnt_extra])
	            CompetitionCnt_extra += 1
	        else:
	            SlideList_extra.append(LectureList_extra[LectureCnt_extra])
	            LectureCnt_extra += 1
	    l1 = result_list + SlideList_extra
	    result_list = sorted(set(l1),key=l1.index) 
	    if(len(result_list) > maxlen):
	        result_list = result_list[0:maxlen]

    return result_list, len(result_list)


