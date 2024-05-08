FROM python:3.12.3-slim-bullseye
RUN mkdir /app
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
EXPOSE 7000
CMD ["python","manage.py","runserver","0.0.0.0:7000"]