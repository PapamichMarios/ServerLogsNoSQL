# ServerLogsNoSQL

A REST API project in Flask & MongoDB for post-graduate class Database Management Systems

# Authors

- [Papadopoulos Christos-Charalampos](https://github.com/Christosc96)
- [Papamichalopoulos Marios](https://github.com/PapamichMarios)

# Tools Used

- Python 3.6.9
- Flask 1.1.1
- MongoDB Community Server 4.2.2
- Faker
- Postman

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

The first one contains all types of logs. We felt it was not correct design principal to furtherly normalize our log collection, since the point of NoSQL is to keep normalization at a minimum. Another reason is that lookups are really costly and one wants to avoid it at all costs.

As a result we have merged all the types of logs into one collection, to avoid using joins for the queries.

The second collection, contains all the admin related data as mentioned in the requirements of the project. In more detail, each admin owns the following properties:

- username
- email
- telephone
- an array of the upvotes casted

All the admin data have been generated using Faker.

# Queries

All the queries can be found at:

```
./ServerLogsFlask/ServerLogsNoSQL/methods.py 
./ServerLogsFlask/ServerLogsNoSQL/insert.py 
```

# Sample Snapshots

We present some sample snapshots without the use of indeces:

- API Query 1
![alt text](api%20snapshots/method1-noIndexSmall.png "Query 1")

- API Query 2
![alt text](api%20snapshots/method2-noIndex.png "Query 2")

- API Query 3
![alt text](api%20snapshots/method3.png "Query 3")

- API Query 4
![alt text](api%20snapshots/method4-noIndex.png "Query 4")

- API Query 5
![alt text](api%20snapshots/method5.png "Query 5")

- API Query 6
![alt text](api%20snapshots/method6.png "Query 6")

- API Query 7
![alt text](api%20snapshots/method7Index.png "Query 7")

- API Query 8
![alt text](api%20snapshots/method8.png "Query 8")

- API Query 9
![alt text](api%20snapshots/method9.png "Query 9")

- API Query 10
![alt text](api%20snapshots/method10.png "Query 10")

- API Query 11
![alt text](api%20snapshots/method11.png "Query 11")

- Insert Log Examples
![alt text](api%20snapshots/insert_access.png "Insert Access Log")
![alt text](api%20snapshots/insert_received.png "Insert Received Log")

- Cast an upvote
![alt text](api%20snapshots/insert_upvote_exists.png "Error Upvote")
![alt text](api%20snapshots/insert_upvote.png "Cast Upvote")

# Indices

## Log_timestamp Index
We found out that indices are situational since only two aggregation pipeline stages (sort, match) take indices into account. Group for example makes no use of it. 

In addition to these, by running time range queries we observed that indices speed up the query when they search for a small time range. We can see that with the following snapshots based on method2:

1. For a small time range query using index makes it faster, to the point that is almost instant:

  * Index 
    ![alt text](api%20snapshots/method2-indexSmall.png "Index method 2")

  * No Index
    ![alt text](api%20snapshots/method2-noIndexSmall.png "Index method 2")

2. For a relatively large time range query we observe that the index gives only a slight boost in most cases:

  * Index
    ![alt text](api%20snapshots/method2-indexBig.png "Index method 2")

  * No Index
    ![alt text](api%20snapshots/method2-noIndexBig.png "Index method 2")

3. Average case:

  * Index
    ![alt text](api%20snapshots/method2-index.png "Index method 2")

  * No Index
    ![alt text](api%20snapshots/method2-noIndex.png "Index method 2")

Despite the not so observable optimization, having a timestamp index is important since most of the queries involve a specific date or time range.

## Type Index

As we see from the snapshot following adding an index on type field gives a slight boot to the query:

- Index
![alt text](api%20snapshots/method2-indexType.png "Index method 2")

- No Index
![alt text](api%20snapshots/method2-noIndexBig.png "Index method 2")

## HTTP Method Index

- Index
![alt text](api%20snapshots/method4-indexHttpMethod.png "Index method 4")

- No Index
![alt text](api%20snapshots/method4-noIndex.png "Index method 4")

## Upvote Index
We also created an index for the upvote field of the admin collection which greatly increased query 7 execution speed

- Index
![alt text](api%20snapshots/method7Index.png "Index method 7")

- No Index
![alt text](api%20snapshots/method7noIndex.png "Index method 7")



Indeces were tested on other fields as well but no noticeable optimizations was indicated. We also created a compound index on log_timestamp and type but it actually made the query slower.

# Github Link

[ServerLogsNoSQL](https://github.com/PapamichMarios/ServerLogsNoSQL)
