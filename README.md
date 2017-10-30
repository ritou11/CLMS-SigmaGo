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
TODO

## Environment
* Python: v3.6.2
* Django: v1.11.6
### Prepare environment

```bash
pip install django
pip install easy_thumbnails django-image-cropping
```

### Before launch

```bash
cd src/CLMS
python manage.py makemigrations
python manage.py migrate
```

### Launch

```bash
cd src/CLMS
python manage.py runserver localhost:8080
```

## License

GPLv3
