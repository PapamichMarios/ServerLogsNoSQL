from pymongo import MongoClient
from faker import Factory
import time
from random import randint

client = MongoClient("mongodb://localhost:27017")
db = client.log_db
admins = []

def create_names(fake):
    for x in range(10000):
        genEmail = fake.email()
        genName = fake.first_name()
        genSurname = fake.last_name()
        genJob = fake.job()
        genCountry = fake.country()
        longitude, latitude, city, abbr, continent = fake.location_on_land()
        admins.append({
            'email': genEmail,
            'name': genName,
            'surname': genSurname,
            'job': genJob,
            'location': {
                    'longitute': float(longitude),
                    'latitude': float(latitude),
                    'city': city,
                    'country': genCountry
                },
            }
        )
        
    db.admin.insert_many(admins)

if __name__ == '__main__':
    fake = Factory.create()
    create_names(fake)