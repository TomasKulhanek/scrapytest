# script to test parsing json of downloaded flats from sreality and generate jsonlines output
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

for jsonline in generate_items(data):
    print(jsonline)        