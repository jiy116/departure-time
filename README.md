# departure-time

Find the five closet muni bus stops near you and buses that are arriving at these stops

* Date: Nextbus API(support geolocation for stops)
* Back-end language: Python(limited experience)
* Web framework: Flask(limited experience)
* DataBase: MongoBD(first time)

You can find the web site here http://departuretime.info

## Things have learned
* Python: Have limited knowledge with python before, be more comfortable coding in python after this execise, learned how to avoid circular dependencies in python; how to parse the XML file
* MongoDB: Learned how to use the mongoDB and how to use python mongoengine to interact with mongoDB, its funcationality and advantages compare to other database and other types of database.
* Flask: More familiar with Flask microframework. 

## Tradeoff
**Accuracy vs Scalability:** to avoid large traffic between web server and database, use mongoDB to cache the recently used bus information for certain time(I pick 60 seconds for convenience), than recalcuate the predicted time base on the old predicted time and esplased time since data be cached. By this way, web server can handle large amount of user request with much fewer interaction with Nextbus's data quotes. User performance also be improved due to small wait time.

## Things that need to be fixed 
* Test, need more tests to fully test the webserver API and find bugs
* Error handling
* More functional API, the API now is too simple to satisfy the real-life requirement
* More attractive front end to delivere the data to users, and the usage of framework
* Mobile support. Considering most users will use smart phones to use this application.

##API
stop.js?lon=\<lon\>&lat=\<lat\>&start=\<n\>&offset=\<m\>

start and offset are optional

start: nth nearest stop, default 0

offset: number of stops, default 5

reutrn stops and predictions infomation
