from fastapi import FastAPI, HTTPException
#from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import psycopg2
from typing import List

app = FastAPI()
# mount static files so that they can be server by fastapi
app.mount("/static", StaticFiles(directory="../frontend/dist",html=True), name="static")
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]
# route default endpoint to static index.html
@app.get("/",response_class=HTMLResponse)
def read_root():
    return "<meta http-equiv='Refresh' content='0; url=/static/index.html' />"

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins,
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)

# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'vagrant',
    'host': 'localhost',
    'port': 5432           # the port mapped in runpostgres.sh script
}

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(**db_params)
    return conn

@app.get("/property", response_model=List[dict])
async def read_properties():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM property_listings;")
    #properties = cursor.fetchall()
    myproperties = []
    for row in cursor.fetchall():
        myproperties.append({'id':row[0],'title':row[1],'image':row[2],'url':row[3]})
    cursor.close()
    conn.close()
    return myproperties

@app.get("/property/{property_id}", response_model=dict)
async def read_property(property_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM property_listings WHERE id = %s;", (property_id,))
    row = cursor.fetchone()
    myproperty ={}
    if row:
        myproperty = {'id':row[0],'title':row[1],'image':row[2],'url':row[3]}
    cursor.close()
    conn.close()
    if row:
        return myproperty
    else:
        raise HTTPException(status_code=404, detail="Property not found")
