from pymongo import MongoClient
from faker import Factory
import time
import random
from random import randint

client = MongoClient("mongodb://localhost:27017")
db = client.log_db
admins = []

def create_names(fake):
    for x in range(3000):    #insert admins number
        genEmail = fake.email()
        genName = fake.first_name()
        genSurname = fake.last_name()
        genPhone = fake.phone_number()
        upvotes = random.randrange(500, 1001)   #insert upvotes range per admin
        pipeline = [{"$sample": {"size": upvotes}}]
        documents = db.log.aggregate(pipeline)
        document_list = list(documents)

        upvotes_list = []

        for doc in document_list:
            upvotes_list.append(doc["_id"])




        admins.append({
            'email': genEmail,
            'username': genName + '_' + genSurname,
            'phone': genPhone,
            'upvotes': upvotes_list
        })
    db.admin.insert_many(admins)

if __name__ == '__main__':
    fake = Factory.create()
    create_names(fake)
