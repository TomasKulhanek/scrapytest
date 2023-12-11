# scripts

`propertyserver.sh`
 to run main server at propertyserver.py

1. use scrapy to get items from sreality server, obey robots.txt
2. store scrapped items into DB (postgresql)
3. start HTTP server use DB (postgresql) to get data
4. frontend with basic list of items in DB at localhost:8000/static/index.html

`property*.py` - scripts related to solution

other `py` and other files - testing scripts produced during incremental development


