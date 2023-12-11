"""
main server to execute
1. executes first scrapy spider to get property list stored in local db
2. executes the fast api server to serve REST Api and provide static HTML frontend to browser
"""


# 1.a initialize db - remove previous data
import propertydb
myconn,mycursor = propertydb.get_postgres_connection()
propertydb.initialize_db()

# 1.b either fill db from local data
propertydb.filldemodata()

propertydb.close_postgres_connection()

# 1.c or execute standalone scrapy to obtain remote data and store them to DB
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from propertyspider import PropertySpider
settings = get_project_settings()
settings.set('ITEM_PIPELINES', {'propertypipeline.PostgresPipeline': 300,})

#process = CrawlerProcess(settings)
#process.crawl(PropertySpider)
#process.start()


#2 execute fast api server to provide access to scrapped data via REST api and static frontend UI
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import psycopg2
from typing import List

app = FastAPI()
# mount static files so that they can be server by fastapi
app.mount("/static", StaticFiles(directory="./static",html=True), name="static")
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]
# route default endpoint to static index.html
@app.get("/",response_class=HTMLResponse)
def read_root():
    return "<meta http-equiv='Refresh' content='0; url=/static/index.html' />"


@app.get("/property", response_model=List[dict])
async def read_properties():
    conn,cursor = propertydb.get_postgres_connection()
    cursor.execute("SELECT * FROM property_listings;")
    #properties = cursor.fetchall()
    myproperties = []
    for row in cursor.fetchall():
        myproperties.append({'id':row[0],'title':row[1],'image':row[2],'url':row[3]})
    propertydb.close_postgres_connection()
    return myproperties

@app.get("/property/{property_id}", response_model=dict)
async def read_property(property_id: int):
    conn,cursor = propertydb.get_postgres_connection()
    cursor.execute("SELECT * FROM property_listings WHERE id = %s;", (property_id,))
    row = cursor.fetchone()
    myproperty ={}
    if row:
        myproperty = {'id':row[0],'title':row[1],'image':row[2],'url':row[3]}
    propertydb.close_postgres_connection()
    if row:
        return myproperty
    else:
        raise HTTPException(status_code=404, detail="Property not found")
