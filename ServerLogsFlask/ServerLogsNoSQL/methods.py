from flask import Blueprint, request
from .extensions import mongo
from flask import jsonify
from datetime import datetime, tzinfo, timezone, timedelta
from bson.json_util import dumps

methods = Blueprint('methods', __name__)

@methods.route('/')
def index():
    return '<h1>Welcome</h1>'


"""
1. Find the total logs per type that were created within a specified time range and sort them in
a descending order. Please note that individual files may log actions of more than one type.
"""
@methods.route('/method1', methods=['GET'])
def getMethod1():

    # get query params
    dayFrom = request.args.get('from')
    dayTo = request.args.get('to')

    if not dayFrom or not dayTo:
        return 'Your url is not valid'
 
    result = mongo.db.log.aggregate([
        {
            '$match': {
                'log_timestamp': {
                    '$gte': datetime.strptime(dayFrom, '%Y-%m-%d %H:%M:%S'),
                    '$lte': datetime.strptime(dayTo, '%Y-%m-%d %H:%M:%S')
                }
            }
        }, {
            '$group': {
                '_id': '$type',
                'total_logs': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'total_logs': -1
            }
        }
    ])

    return dumps(result)
    
"""
2. Find the number of total requests per day for a specific log type and time range.
"""
@methods.route('/method2', methods=['GET'])
def getMethod2():

    # get query params
    dayFrom = request.args.get('from')
    dayTo = request.args.get('to')
    logType = request.args.get('type')

    if not dayFrom or not dayTo or not logType:
        return 'Your url is not valid'

    result = mongo.db.log.aggregate([
        {
            '$match': {
                'type': logType, 
                'log_timestamp': {
                    '$gte': datetime.strptime(dayFrom, '%Y-%m-%d %H:%M:%S'), 
                    '$lte': datetime.strptime(dayTo, '%Y-%m-%d %H:%M:%S')
                }
            }
        }, {
            '$project': {
                'day': {
                    '$dateToString': {
                        'format': '%Y-%m-%d', 
                        'date': '$log_timestamp'
                    }
                }
            }
        }, {
            '$group': {
                '_id': '$day', 
                'requests': {
                    '$sum': 1
                }
            }
        }
    ])

    return dumps(result)

"""
3. Find the three most common logs per source IP for a specific day.
"""
@methods.route('/method3', methods=['GET'])
def getMethod3():
    
    # get query params
    day = request.args.get('day')
    day = datetime.strptime(day, '%Y-%m-%d')
    day = day.strftime("%Y-%m-%d")

    result = mongo.db.log.aggregate(
        [
            {
                '$project': {
                    'day': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$log_timestamp'
                        }
                    },
                    'source_ip': '$source_ip',
                    'type': '$type'
                }
            }, {
            '$match': {
                'day': day
            }
        }, {
            '$group': {
                '_id': {'type':'$type','source_ip':'$source_ip'},
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$project': {
                '_id': '$_id.source_ip',
                'type': '$_id.type',
                'count': '$count' }

        }, {
            '$sort':{
                '_id':-1,
                'count':-1
            }
        }, {
            '$group': {
                '_id': '$_id',
                'counts': {
                    '$push': {'count':'$count', 'type':'$type'}
                }
            }
        },{
            '$project':{'counts':{ '$slice':['$counts',3]}}
        }

        ], allowDiskUse=True
    )

    return dumps(result)

"""
4. Find the two least common HTTP methods with regards to a given time range.
"""
@methods.route('/method4', methods=['GET'])
def getMethod4():
    
    # get query params
    dayFrom = request.args.get('from')
    dayTo = request.args.get('to')

    if not dayFrom or not dayTo:
        return 'Your url is not valid'

    result = mongo.db.log.aggregate([
        {
            '$match': {
                'log_timestamp': {
                    '$gte': datetime.strptime(dayFrom, '%Y-%m-%d %H:%M:%S'), 
                    '$lte': datetime.strptime(dayTo, '%Y-%m-%d %H:%M:%S')
                }
            }
        }, {
            '$group': {
                '_id': '$http_method', 
                'total': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'total': 1
            }
        }, {
            '$limit': 2
        }
    ])

    return dumps(result)

"""
5. Find the referers (if any) that have led to more than one resources.
"""
@methods.route('/method5', methods=['GET'])
def getMethod5():

    result = mongo.db.log.aggregate([
        {
            '$group': {
                '_id': '$referer',
                'count': {
                    '$sum': 1
                },
                'resources': {
                    '$addToSet': '$resource'
                }
            }
        }, {
            '$project': {
                'referer': '$_id',
                '_id': 0,
                'size': {
                    '$size': '$resources'
                }
            }
        }, {
            '$match': {
                'size': {
                    '$gt': 1
                }
            }
        }
    ])

    return dumps(result)

"""
6. Find the blocks that have been replicated the same day that they have also been served.
"""
@methods.route('/method6', methods=['GET'])
def getMethod6():
    
    result = mongo.db.log.aggregate([
        {
            '$match': {
                '$or': [
                    {
                        'type': 'replicate'
                    }, {
                        'type': 'served'
                    }
                ]
            }
        }, {
            '$unwind': {
                'path': '$blocks'
            }
        }, {
            '$group': {
                '_id': {
                    'block': '$blocks', 
                    'day': {
                        '$dateToString': {
                            'format': '%Y-%m-%d', 
                            'date': '$log_timestamp'
                        }
                    }, 
                    'type': '$type'
                }
            }
        }, {
            '$group': {
                '_id': {
                    'block': '$_id.block', 
                    'day': '$_id.day'
                }, 
                'types': {
                    '$sum': 1
                }
            }
        }, {
            '$match': {
                'types': 2
            }
        }, {
            '$project': {
                '_id': 0, 
                'block': '$_id.block'
            }
        }
    ])

    return dumps(result)


"""
7. Find the fifty most upvoted logs for a specific day.
"""
@methods.route('/method7', methods=['GET'])
def getMethod7():

    #get query params
    day = request.args.get('day')
    day = datetime.strptime(day, '%Y-%m-%d')
    day = day.strftime("%Y-%m-%d")


    result = mongo.db.log.aggregate([
        {
            '$project': {
                'day': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$log_timestamp'
                    }
                },
            }
        },
        {
            '$match': {
                'day': day
            }
        }, {
            '$lookup': {
                'from': 'admin',
                'localField': '_id',
                'foreignField': 'upvotes',
                'as': 'string'
            }
        }
        , {
           '$project': {
                'total': {
                     '$size': '$string'
                },
             }
         }
         ,{
            '$sort': {
                'total': -1
             }
         }, {
             '$limit': 50
         }])

        #
        # {
        #     '$unwind': {
        #         'path': '$upvotes'
        #     }
        # }, {
        #     '$lookup': {
        #         'from': 'log',
        #         'localField': 'upvotes',
        #         'foreignField': '_id',
        #         'as': 'string'
        #     }
        # },{
        #     '$unwind': {
        #         'path': '$string'
        #     }
        # },{
        #         '$project': {

        #             'day': {
        #                 '$dateToString': {
        #                     'format': '%Y-%m-%d',
        #                     'date': '$string.log_timestamp'
        #                 }
        #             },
        #             'upvote':'$string._id',
        #             'source_ip': '$string.source_ip',
        #         }
        #     }, {
        #     '$match': {
        #         'day': day
        #     }
        # },{
        #     "$group": {
        #     "_id": "$upvote",
        #     "count": { "$sum": 1 }
        #     }
        # }, {
        #     '$sort': {
        #         'count': -1
        #     }
        # }, {
        #     '$limit': 50
        # }

    return dumps(result)

"""
8. Find the fifty most active administrators, with regard to the total number of upvotes.
"""
@methods.route('/method8', methods=['GET'])
def getMethod8():
    
    result = mongo.db.admin.aggregate([
        {
            '$project': {
                'upvotes': {
                    '$size': '$upvotes'
                }
            }
        }, {
            '$sort': {
                'upvotes': -1
            }
        }, {
            '$limit': 50
        }
    ])

    return dumps(result)

"""
9. Find the top fifty administrators, with regard to the total number of source IPs for which
they have upvoted logs.
"""
@methods.route('/method9', methods=['GET'])
def getMethod9():

    result = mongo.db.admin.aggregate([
        {
            '$unwind': {
                'path': '$upvotes'
            }
        }, {
            '$lookup': {
                'from': 'log',
                'localField': 'upvotes',
                'foreignField': '_id',
                'as': 'string'
            }
        },{
            "$group": {
            "_id": "$_id",
            "distinct_ips": { "$addToSet": "$string.source_ip" }
            }
        },{
            '$project': {
            'total_ips': {
                    '$size': '$distinct_ips'
                }
            }
        }, {
            '$sort': {
                'total_ips': -1
            }
        }, {
            '$limit': 50
        }
    ], allowDiskUse=True)
    
    return dumps(result)

"""
10. Find all logs for which the same e-mail has been used for more than one usernames when
casting an upvote.
"""
@methods.route('/method10', methods=['GET'])
def getMethod10():
    
    result = mongo.db.admin.aggregate([
        {
            '$group': {
                '_id': '$email', 
                'upvotes': {
                    '$push': '$upvotes'
                }, 
                'total': {
                    '$sum': 1
                }
            }
        } , {
            '$match': {
                'total': {
                    '$gt': 2
                }
            }
        }, {
            '$unwind': {
                'path': '$upvotes'
            }
        }, {
            '$unwind': {
                'path': '$upvotes'
            }
        }, {
            '$group': {
                '_id': '$upvotes'
            }
        }
    ], allowDiskUse=True)

    return dumps(result)

"""
11. Find all the block ids for which a given name has casted a vote for a log involving it.
"""
@methods.route('/method11', methods=['GET'])
def getMethod11():

    # get query params
    username = request.args.get('name')
    
    result = mongo.db.admin.aggregate([
        {
            '$match': {
                'username': username
            }
        },
        {
            '$unwind': {
                'path': '$upvotes'
            }
        }, {
            '$lookup': {
                'from': 'log',
                'localField': 'upvotes',
                'foreignField': '_id',
                'as': 'string'
            }
        }, {
            '$unwind': {
                'path': '$string'
            }
        },{
            '$match': {
                'string.blocks': {
                    '$ne': None
                }
            }
        },{
            '$match': {
                'string.blocks': {
                    '$ne': []
                }
            }
        },{
            '$project':{
                "_id":0,
                'blocks':'$string.blocks'
            }
        }])

    return dumps(result)