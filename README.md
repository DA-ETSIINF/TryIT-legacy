# TryIT!
Source code for the Try IT! website.

Official website: https://congresotryit.es/
## TravisCI
-- ??
## Dependencies
- Python 3.5.3
- Django 2.1.7
- django-backup 1.0.1
- djangorestframework 3.7.1
- gunicorn 19.7.1
- olefile 0.44
- Pillow 5.4.1
- pytz 2018.7
- reportlab 3.4.0
- pip 19.0.1

## Installation

### Linux 
1\. Install python 3.5 and pip
```bash
$ sudo apt install python3.5
$ sudo apt install python-pip
```
Also upgrade pip if necessary
```bash
$ pip install --upgrade pip
```
2\. Create a virtual environment with python 3.5

First install virtualenvwrapper
```bash
$ sudo apt install virtualenvwrapper
```
Then create a virtual environment
```bash
$ mkvirtualenv --python=/usr/bin/python3.5 tryIt
```
If it is not automatically activated then, activate it
```bash
$ workon tryIt
```
3\. Install the requirements
```bash
$ pip install -r requirements.txt
```

## Windows 
1\. Download and install python 3.5 from the [official web page](https://www.python.org/downloads/windows/)

2\. Install pip
```bash
> py -m pip install
```
Also upgrade pip if necessary
```bash
> py -m pip install --upgrade pip
```
3\. Create a virtual environment with python 3.5

First install virtualenv
```bash
> py -m pip install --user virtualenv
```
Then create the virtual environment
```bash
> py -m virtualenv tryIt
```
If it is not automatically activated, then activate it
```bash
> .\tryIt\Scripts\activate
```
4\. Install the requirements

-- There is no requirements file at the moment (in the main directory)
```bash
 > pip install -r requirements.txt
```
## Mac 

### Docker
-- ???
## Run

### DB
First of all you need to execute this commands to set up the DB
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```
#### Create from scratch
After doing the previous step, you must create a super user for the DB
```bash
$ python manage.py createsuperuser
```
Once you have the super user created, go to `http://127.0.0.1:8000/admin/`, introduce the user and password and you can start creating the items for the DB
#### Examples
-- Should I add a video creating some items?
 
### Linux (via terminal)
With your virtualenv activated, you can run `python manage.py runserver` or `./manage.py runserver` if it has execute permission.

Then you can go to the url `http://127.0.0.1:8000`.

### Windows (via terminal)
With your virtualenv activated, you can run `python manage.py runserver`.

Then you can go to the url `http://127.0.0.1:8000`.

### Pycharm
-- ??
#### Normal
-- ??
#### Docker
1\. Move to the [docker-dev](/docker-dev) directory
```bash
$ cd docker-dev
```
2\. Build the dev image 
```bash
$ docker build -t tryit-web-dev .
```
3\. Run this compose 
```bash
$ docker-compose up -d
```
4\. Run bash in the image 
```bash
$ docker-compose exec web bash
```
5\. Run Django
```bash
$ python manage.py runserver 0.0.0.0:8000
```
Then you can go to the url `http://0.0.0.0:8000`.
## License
-- Create LICENSE and link it here

## Authors
- [Alejandro Otero](https://github.com/lexotero)
- [Álvaro Manzanas](https://github.com/alvarogtx300)
- [Sergio Valverde](https://github.com/svg153)
- [Máximo García](https://github.com/onmax)
- [Daniel Martín](https://github.com/mdmoreno)
- [Samuel García](https://github.com/samgh96)
- [Diego Fernández](https://github.com/diegofpb)
- [Víctor Nieves](https://github.com/VictorNS69)
- [Javier Barragán](https://github.com/JavierBH)
