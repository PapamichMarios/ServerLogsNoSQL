# ServerLogsNoSQL

A REST API project in Flask & MongoDB for post-graduate class Database Management Systems

# Authors

- [Papadopoulos Christos](https://github.com/Christosc96)
- [Papamichalopoulos Marios](https://github.com/PapamichMarios)

# Tools Used

- Python 3.6.9
- Flask 1.1.1
- MongoDB Community Server 4.2.2
- Faker

# How to run

- populate the database by running the scripts:

```
populateAdmins.py
```
and

```
populateLogs.py
```
inside ```logs``` directory

- traverse inside the directory

- type in your terminal:

``` 
. flask-mongodb/bin/activate
```
or set up a virtual environment downloading:

```flash flask-pymongo```

- start the REST API:

```
flask run
```

- app is up and running on 

```
http://127.0.0.1:5000/ 
```

# Schema Design

Our database consists of two primary collections:

- log 

- admin

The first one contains all types of logs. We felt it was not correct design principal to furtherly normalize our log collection, since the point of NoSQL is to keep normalization at a minimum. 

As a result we have merged all the types of logs into one collection, to avoid using joins for the queries.

The second collection, contains all the admin related data as mentioned in the requirements of the project. In more detail, each admin owns the following properties:

- username
- email
- telephone
- an array of the upvotes casted

All the admin data have been generated using Faker.

# Indices

# Queries

All the queries are available at:

```
api-methods.txt
```

# Sample Snapshots

# Github Link

[ServerLogsNoSQL](https://github.com/PapamichMarios/ServerLogsNoSQL)
