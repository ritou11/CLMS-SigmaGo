# Competition & Lecture Management System by SigmaGo
This is a task in the course Software Engineering 2017, Tsinghua University.

## Group Member
* Xiufeng Huang, EE, THU, 2014;
* Haidong Zhu, EE, THU, 2015;
* Yining Cao, SE, THU, 2015;
* Haotian Liu, EEA, THU, 2014;
* Yizeng Han, DA, THU, 2014;
* Zhixing Zhang, MSE, THU, 2015;

## Introduction
(TODO: Translation) 针对于校园中讲座和竞赛资源的流通性不足、同学们获取信息和资源的方式过于分散等问题，我们小组希望能够设计一个竞赛讲座管理系统，通过对于竞赛、讲座等信息进行统一整理和总结，并且设计一种算法对于特定同学进行合适的讲座和竞赛的推荐，增加同学们对于自己所需要的讲座、感兴趣的竞赛的认知，从而实现信息的最大化利用。

## Environment
* Python: v3.6.2
* Django: v1.11.6
### Prepare environment

```bash
pip install django
pip install easy_thumbnails django-image-cropping
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple wechat-sdk
```

### Before launch

```bash
cd src/CLMS
python manage.py makemigrations
python manage.py migrate
```

Create ```secert.py``` in ```src/CLMS/``` , and add the following content.

```python
class Secret():

    SECRET_TOKEN = 'YOUR_TOKEN'
    APP_ID = 'YOUR_ID'
    APP_SECRET = 'YOUR_SECRET'
    ENCODING_AES_KEY = 'YOUR_KEY'
    HOME_URL = 'http://YOUR_URL'

```

If you want to deploy it online, you should add your server ip in WEIXIN's IP whitelist.

### Launch

```bash
cd src/CLMS
python manage.py runserver localhost:8080
```

### Fix after updates

```bash
cd src/CLMS
python manage.py migrate --run-syncdb
```

## Tips

### Migrate Frontend Code

Regex replace ```src=((?!.*http)".+?")``` to ```src={% static $1 %}```.
Regex replace ```href=((?!.*(\#|http))".+?")``` to ```href={% static $1 %}```.

## License

GPLv3
