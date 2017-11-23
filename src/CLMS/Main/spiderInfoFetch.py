import requests
from bs4 import BeautifulSoup

def stuClassesInfo(userName,password):
    '''
    Fetch personal information and course information from weblearn.
    :param userName: student's id
    :param password: password
    :return: (list)CourseList + (dict)PersonalInfo
    '''
    loginSession = requests.session()
    loginData = {'userid':userName, 'userpass':password}
    webLearnUrl = 'https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
    coursesUrl = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?language=cn'
    loginSession.post(webLearnUrl,loginData)
    courseInfo = loginSession.get(coursesUrl)
    courseText = BeautifulSoup(courseInfo.text,'html.parser')
    classRawList = courseText.find_all(name = 'tr', class_ = 'info_tr2') \
                + courseText.find_all(name = 'tr', class_ = 'info_tr')
    courseList = []
    for singleClass in classRawList:
        courseInfo = singleClass.get_text().split()
        courseInfo = courseInfo[0][0:-15]                                       # delete the semester
        courseList.append(courseInfo)

    personUrl = 'http://learn.tsinghua.edu.cn/MultiLanguage/vspace/vspace_userinfo1.jsp'
    personRawInfo = loginSession.get(personUrl)
    personRawInfo = BeautifulSoup(personRawInfo.text,'html.parser')
    print(personRawInfo)
    perInfoRawList = personRawInfo.find_all(name='td', class_='tr_l') + personRawInfo.find_all(name='td', class_='tr_l2')
    personalInfo = {}
    infoCount = 0
    for singleInfo in perInfoRawList:
        singleInfo = singleInfo.get_text().split()[0]
        if infoCount == 0:
            personalInfo['stuID'] = int(singleInfo)
        elif infoCount == 2:
            personalInfo['poliVisage'] = singleInfo
        elif infoCount == 3:
            personalInfo['email'] = singleInfo
        elif infoCount == 7:
            personalInfo['stuType'] = singleInfo                    # Undergraduate or graduate student
        elif infoCount == 8:
            personalInfo['stuName'] = singleInfo
        elif infoCount == 9:
            personalInfo['nation'] = singleInfo
        elif infoCount == 11:
            personalInfo['phoneNum'] = int(singleInfo)
        infoCount += 1
    return courseList,personalInfo

def stuPersonalInfo(userName,password):
    #to be continue
    pass

if __name__ == '__main__':
    stuClassesInfo('zhuhd15','DL_15Conca')
