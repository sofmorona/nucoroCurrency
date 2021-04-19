# NucoroCurrency
---
<br>  
<br>

## Index

---
##### [Introduction](#intro)
##### [Dependencies](#dependencies)
##### [Setup](#setup)
##### [How to use](#howtouse)
##### [improvements](#changelog)


<br>  
<br>
 
## Introduction <a name="intro"></a>

---
API that allows users to calculate currency exchange rates.
* Service to retrieve a List of currency rates for a specific time period
* Service that Calculates (latest) amount in a currency exchanged into a different currency.
* Service to retrieve time-weighted rate of return for any given amount invested from a currency into another one from given date until today.  

<br>  
<br>

## Dependencies <a name="dependencies"></a>

---
To execute the web server you must have python3 in your system.
The following libraries are needed.  

| Requirement | Version | Description |
|:-------|:------------|:------------|
|Python | 3.6 | Python 3.6 or higher needed |
|Django | 3.2 | Django Framework |
|Django Rest Framework | 3.12.4 | Framwork to build a REST API with Django|
|requests | 2.25.1 | Library for HTTP requests |
|celery | 5.0.5 | Library to create tasks|
<br>  
<br>


## Setup  <a name="setup"></a>

---
We recommend create a virtual enviroment to isolate the application.

<br>  
<br>

##### Create virtual enviroment:

---
* In case we don't have virtualenv installed in the system we have to install it.
```
 $ sudo pip install virtualenv 
 ```
* Now we create the virtual env in our project folder root.
```
$ python3 -m venv env
```
* And activate it
** For Linux / Macos
```
$ source env/bin/activate
```
** For windows
```
env\Scripts\activate
```
* Once we have the virtual env activated we install the dependencies
```
$ pip install -r requirements.txt
```
* To config the DB and create an initial user
```
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
```
* To populate the DB with the initial data
```
python manage.py loaddata CurrencyType
python manage.py loaddata ProvidersType
```

* To start the webserver
```
python manage.py runserver
```

<br>  
<br>

## How to use Nucoro Currency  <a name="howtouse"></a>

---
Once you have the server running you can request for the API Endpoints.
In the code you can find a postman collection with a sample of each API Endpoint.


<br>  
<br>
 
## Improvements  <a name="improvements"></a>

---
* Implement all requirements, right now only the structure is almost done.
* The database should be changed to a more stable DB like PostgreSQL, MySQL, etc.
* The server should be changed to a one more stable like Nginx or Apache.
* Add log to each request to be able to traceback possible errors.
* Config the pagination for the requests.
* Improve the checking about date ranges, right now if I have only one item in the selected range I return it, but would be better return all values in the selected range.


<br>  
<br>
