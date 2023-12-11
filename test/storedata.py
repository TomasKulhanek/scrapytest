# script to test parsing and storing json to DB, file is predownloaded flats from sreality
import json

test_file_path = 'byty.json'
test_url_prefix = 'https://www.sreality.cz/api'


with open(test_file_path, 'r') as file:
    data = json.load(file)

#print(data)
def generate_items(jsondata):
    for estate in jsondata['_embedded']['estates']:
        yield {
            "title": estate['name']+" "+estate['locality'],
            "image": estate['_links']['images'][0]['href'],
            "url": test_url_prefix+estate['_links']['self']['href']
        }

import psycopg2
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'vagrant',
    'host': 'localhost',
    'port': 5432           # the port mapped in runpostgres.sh script
}

# Connect to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()
# Create a new table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS property_listings (
        id SERIAL PRIMARY KEY,
        title TEXT,
        image TEXT,
        url TEXT
    );
''')
conn.commit()
# delete all previous data
query = "DELETE FROM property_listings;"
cursor.execute(query)
conn.commit()

# Insert data into the table
for flat in generate_items(data):
    #data = json.loads(line)
    cursor.execute('''
        INSERT INTO property_listings (title, image, url) VALUES (%s, %s, %s)
    ''', (flat['title'], flat['image'], flat['url']))

# Commit and close the connection
conn.commit()
cursor.close()
conn.close()
print("Data inserted successfully.")