"""
Pipeline for SCRAPY framework
stores processed property into shared DB
"""
import propertydb

class PostgresPipeline(object):

    def open_spider(self, spider):
        self.connection, self.cur = propertydb.get_postgres_connection()        

    def close_spider(self, spider):     
        print("Data scrapped and inserted successfully.")   
        propertydb.close_postgres_connection()

    def process_item(self, property, spider):
        #self.cur.execute("INSERT INTO your_table(url, ...) VALUES (%s, ...)", (item['url'], ...))
        self.cur.execute("INSERT INTO property_listings (title, image, url) VALUES (%s, %s, %s)",
                          (property['title'], property['image'], property['url']))
        self.connection.commit()
        return property