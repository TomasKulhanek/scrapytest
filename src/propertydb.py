"""
Shared DB connection and cursor functions
functions:
    get_postgres_connection(): returns conn and cursor
    initialize_db(): create table 'property_listing' and delete all data if it is there from previous run
    close_postgres_connection(): close the shared connection and cursor, call it once at the end off session
"""
import psycopg2
scdbconn = None
scdbcursor = None

def get_postgres_connection():
    global scdbconn,scdbcursor
    # return if already initialized
    if (scdbconn is not None):
        return scdbconn, scdbcursor
    # Define your connection parameters
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'vagrant',
        'host': 'localhost',
        'port': 5432           # the port mapped in runpostgres.sh script
    }
    try:
        # Establish a connection to the database
        scdbconn = psycopg2.connect(**db_params)
        # Create a cursor object
        scdbcursor = scdbconn.cursor()
        # now create table - delete all previous data

        return scdbconn, scdbcursor
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None, None

def initialize_db():
    global scdbconn,scdbcursor
    scdbcursor.execute('''
            CREATE TABLE IF NOT EXISTS property_listings (
                id SERIAL PRIMARY KEY,
                title TEXT,
                image TEXT,
                url TEXT
            );
        ''')
    scdbconn.commit()
    # delete all previous data - TODO consider to update ???       
    scdbcursor.execute("DELETE FROM property_listings;")
    scdbconn.commit()
    
def close_postgres_connection():
    global scdbconn,scdbcursor
    # Close the cursor and connection
    if (scdbconn is not None):
        scdbcursor.close()
        scdbconn.close()
        scdbcursor = None
        scdbconn = None
    else:
        print("Database connection can't be closed before inititialization.")

def filldemodata():
    import json
    global scdbconn,scdbcursor

    test_file_path = 'byty.json'
    test_url_prefix = 'https://www.sreality.cz/api'


    with open(test_file_path, 'r') as file:
        data = json.load(file)
    def generate_items(jsondata):
        for property in jsondata['_embedded']['estates']:
            yield {
                "title": property['name']+" "+property['locality'],
                "image": property['_links']['images'][0]['href'],
                "url": test_url_prefix+property['_links']['self']['href']
            }
    # Insert data into the table
    for property in generate_items(data):
        #data = json.loads(line)
        scdbcursor.execute('''
            INSERT INTO property_listings (title, image, url) VALUES (%s, %s, %s)
        ''', (property['title'], property['image'], property['url']))

    # Commit and close the connection
    scdbconn.commit()        
    print("Data inserted successfully.")