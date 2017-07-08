# Attendance Management
Attendance Management minimalist framework

## Tech Stack
Development Language: Python
Web Framework: Flask
Database ORM: SQLAlchemy
Database: SQLITE

1. Create a virtualenv using virtualenvwrapper: `mkvirtualenv att_management`
2. Install requirements: `pip install -r requirements.txt`
3. Create database: `python db_create.py`
4. Create Migration: `python db_migrate.py`
5. `python run.py`

# Routes Expossed: </br>
## Attendance:</br>
`GET` /attendance/ - Listing attendance </br>
`POST` /attendance/ - Marks start or end of the day </br>


## Breaks:</br>
`POST` /breaks/ - Marks start or end of break </br>

## Deployment


### Base Docker Image

* [ubuntu:12.04](https://registry.hub.docker.com/_/ubuntu/)


### Installation

1. Install [Docker](https://www.docker.com/).


```bash
docker build -t attendance_management .
```


### Usage

```bash
docker run -d -p 80:80 attendance_management
```

After few seconds, open `http://<host>` to see the Flask app.