import skimage.io
from skimage.transform import resize
from Main.models import *

def make_thumb(path, thumb_path, size=(160, 120)):
    image = skimage.io.imread(path)
    height, width = image.shape[0], image.shape[1]

    thumb = image

    if (height / width) > (size[0] / size[1]):
        new_height = width * size[0] / size[1]
        height1 = (height - new_height) / 2
        thumb = image[height1:height + new_height, 0:width]

    if (height / width) < (size[0] / size[1]):
        new_width = height * size[1] / size[0]
        width1 = (width - new_width) / 2
        thumb = image[0:int(height), int(width1):int(width1 + new_width)]

    thumb = resize(thumb, size)
    print(thumb.shape)
    skimage.io.imsave(thumb_path, thumb)
    return thumb

def recommend_list(request,maxlen):
    try:
        user = User.objects.get(username=request.session['user_id'])
    except:
        return None,0
    CompetitionList = Competition.objects.filter(
        tag__name='a tag you will never use')
    LectureList = Lecture.objects.filter(tag__name='a tag you will never use')
    for tag in user.interestTag.all():
        try:
            CompetitionList = CompetitionList | Competition.objects.filter(
                tag__name=str(tag))
        except Competition.DoesNotExist:
            raise Http404
        try:
            LectureList = LectureList | Lecture.objects.filter(tag__name=(tag))
        except Lecture.DoesNotExist:
            raise Http404
    CompetitionList.distinct()
    LectureList.distinct()
    result_list = []
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
    return result_list,len(CompetitionList)+len(LectureList)