# Attendance Management
Attendance Management minimalist framework

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
