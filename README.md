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
In response to the lack of liquidity in lecture and competition information on campus and the students' excessive access to information and resources, our team hopes to design a competition management system to organize and summarize information on competitions and lectures. And an algorithm is designed to recommend appropriate lectures and competitions for specific students, so as to increase the students' awareness of the lectures they are interested in and the competitions they are interested in, so as to maximize the use of information.

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
    ENCODING_AES_KEY = 'YOUR_KEY'
    HOME_URL = 'http://YOUR_URL'

```

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

### Create docker machine

```bash
docker-machine create --driver=generic --generic-ip-address=YOUR_IP qcloud(your name)
eval $(docker-machine env qcloud)
```

### Deploy

```bash
cd src/CLMS/
docker-compose up -d --build
```

## License

GPLv3
