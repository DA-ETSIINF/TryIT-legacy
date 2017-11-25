FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE TryIT.settings
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
