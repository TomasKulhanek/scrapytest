# Scrapytest

  * `src/` contains backend scripts and static frontend served by the fast api
  * `frontend/` contains source code of webcomponent used to create simple frontend (aurelia framework used, but transpiled to framework agnostic webcomponents)
  * `test/` other files used for testing scripts during incremental development

`src/propertyserver.sh`
 to run main server at propertyserver.py

1. it uses scrapy to get items from sreality server, obey robots.txt
2. it stores scrapped items into DB (postgresql)
3. it starts HTTP server (fast-api) use DB (postgresql) to get data
4. frontend with basic list of items in DB at localhost:8000/static/index.html

`src/propertydb.py`
Shared DB connection and cursor functions

functions:
  *  get_postgres_connection(): returns conn and cursor
  *  initialize_db(): create table 'property_listing' and delete all data if it is there from previous run
  *  close_postgres_connection(): close the shared connection and cursor, call it once at the end off session

`src/propertypipeline.py`
Pipeline for SCRAPY framework
stores processed property into shared DB

`src/propertyspider.py`
Spider of SCRAPY framework, gets properties from external URL and extract only data that is relevant for our app

`frontend/src/sc/propertylist.*`
Webcomponent to fetch data from REST API and show each property as a card with image, title, and URL pointing to external detail - refers to JSON data / not HTML

# to run in docker
 
  * `git clone ...`
  * `docker-compose up` - this should start DB and FAST API server (propertyserver.py) in docker instance
  *  Open http:/localhost:8000 in your browser.
  The http:/localhost:8000 should redirect to static index.html showing cards of properties in DB. The http://localhost:8000/property gives REST API access to properties listed in DB.
As the server starts up it: 
  1. tries to connect to database first two attempts to localhost - in docker compose there is docker instance of postgresql db
  2. executes first scrapy spider to get property list from remote URL (sreality) and store them in DB
  3. executes the fast api server to serve REST Api and provide static HTML frontend to browser


# to run locally

  ```bash
  git clone ...
  cd src
  ./runpostgres.sh
  ./propertyserver.sh
  ```
And access http://localhost:8000 in your browser

# note

After each start - sreality server is scrapped for 500 new properties, do not run it too much time in order not to be blocked/banned.

