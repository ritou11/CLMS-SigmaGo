FROM python:3.6

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate
RUN python manage.py migrate --run-syncdb
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
