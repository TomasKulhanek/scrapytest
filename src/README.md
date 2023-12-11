# scripts

`propertyserver.sh`
 to run main server at propertyserver.py

1. use scrapy to get items from sreality server, obey robots.txt
2. store scrapped items into DB (postgresql)
3. start HTTP server use DB (postgresql) to get data
4. frontend with basic list of items in DB at localhost:8000/static/index.html

`property*.py` - scripts related to solution

other `py` and other files - testing scripts produced during incremental development

# to run in docker

  * `docker-compose up` - this should start DB and FAST API server (propertyserver.py) in docker instance

# to run locally

1. start postgresql:  `src/runpostgres.sh` which starts docker image of postgres on port 5432
2. start propertyserver: `src/propertyserver.sh`

# note

After each start - sreality server is scrapped for 500 new properties, do not run it too much time in order not to be blocked/banned.

