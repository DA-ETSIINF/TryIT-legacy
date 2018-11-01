FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE TryIT.settings
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

VOLUME /code
COPY ./entrypoint.sh /
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
# in .env file
# ENV DJANGO_SETTINGS_MODULE="TryIT.settings_dev"
