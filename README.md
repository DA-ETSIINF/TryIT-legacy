# TryIT!
-- Descritpion ??

## TravisCI
-- ??
## Dependencies
- Python 3.5.3
- Django 1.11.6
- django-backup 1.0.1
- djangorestframework 3.7.1
- gunicorn 19.7.1
- olefile 0.44
- Pillow 4.3.0
- pytz 2017.2
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
```bash
$ mkvirtualenv --python=/usr/bin/python3.5 tryIt
```
If it is not automatically activated then, activate it
```bash
$ workon tryIt
```
3\. Install the requirements

-- There is no requirements file at the moment (in the main directory)
```bash
$ pip install -r requirements.txt
```

## Windows 

## Mac 

### Docker
-- ???
## Run

### DDBB

#### Create from scratch

#### Examples

### Linux (via terminal)
Run `python manage.py runserver` or `./manage.py runserver` if it has execute permission.

### Windows (via terminal)
Run `python manage.py runserver`.

### Pycharm
-- ??
#### Normal
-- ??
#### Docker
-- ??
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

## Usage

* Dev: Go to `docker-dev/` folder, and read the [README.org](./docker-dev/README.org).
* Production: Go to `docker-production/` folder, and read the [README.org](./docker-production/README.org).