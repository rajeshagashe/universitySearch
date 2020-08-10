# University Search API


### Installation


```sh
$ git clone https://github.com/rajeshagashe/universitySearch.git
$ cd universitySearch
$ pipenv shell
$ pipenv install -r requirements.txt
```
update database url in env.example
```sh
$ mv env.example .env
$ export FLASK_APP=app

```

Create postgres database at localhost:5432/universities
### DB Migration
```sh
$flask db init
$flask db migrate
$flask db upgrade
```
### Run

```sh
$flask run
```

### End-Points

1. /crud/create
    method - POST
    body - {
"alpha_two_code": 'str',
"country": 'str',
"domain": 'str',
"name": 'str',
"web_page": 'str'
}

2. /crud/read/<record_id>  (for one record)
/crud/read  (for all records)
method - GET

3. /crud/update/<record_id> 
method - PATCH
body - {
    key : value,
}

4. /crud/delete/<int:record_id>
method - DELETE

5. /search/universities
 method - POST
 body - {
'name': 'str',
'country_codes': ['str'],
'domains': ['str'],
'limit': 'int',
'offset': 'int'
}
