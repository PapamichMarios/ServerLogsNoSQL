from flask import Blueprint, request
from .extensions import mongo
from flask import jsonify
from datetime import datetime, tzinfo, timezone
from bson.json_util import dumps

methods = Blueprint('methods', __name__)

@methods.route('/')
def index():
    return '<h1>Welcome</h1>'

@methods.route('/method1', methods=['GET'])
def getMethod1():
    dayFrom = request.args.get('from')
    dayTo = request.args.get('to')

    if not dayFrom or not dayTo:
        return 'Your url is not valid'

    logCollection = mongo.db.log
    result = logCollection.aggregate([
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

    return '<pre>' + dumps(result,indent=2) + '</pre>'
    
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

    return '<pre>' + dumps(result,indent=2) + '</pre>'

@methods.route('/method3', methods=['GET'])
def getMethod3():
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
                'day': '2008-11-18'
            }
        }, {
            '$group': {
                '_id': {'type':'$type','source_ip':'$source_ip'},
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$project':{
                '_id': '$_id.source_ip',
                'typeAndCount': {'type':'$_id.type','count':'$count' }
            }
        }, {
            '$group': {
                '_id': '$_id',
                'typesAndCounts': {
                    '$addToSet':'$typeAndCount'}
                }
        }, {
            '$unwind':'$typesAndCounts'
        }, {
            '$sort':{ 'typesAndCounts.count':-1 }
        }, {
            '$group': {
                '_id':'$_id',
                'most_common': {
                    '$addToSet': '$typesAndCounts'
                }
            }
        }

        ], allowDiskUse=True
    )

    return '<pre>' + dumps(result, indent=2) + '</pre>'

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

    return '<pre>' + dumps(result,indent=2) + '</pre>'

@methods.route('/method5', methods=['GET'])
def getMethod5():
    logCollection = mongo.db.log
    result = logCollection.aggregate([
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

    return '<pre>' + dumps(result,indent=2) + '</pre>'

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

    return '<pre>' + dumps(result,indent=2) + '</pre>'


@methods.route('/method7', methods=['GET'])
def getMethod7():
    day = request.args.get('day')
    day = datetime.strptime(day, '%Y-%m-%d')
    day = day.strftime("%Y-%m-%d")
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
            '$unwind': {
                'path': '$string'
            }
        },{
                '$project': {

                    'day': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$string.log_timestamp'
                        }
                    },
                    'upvote':'$string._id',
                    'source_ip': '$string.source_ip',
                }
            }, {
            '$match': {
                'day': day
            }
        },{
            "$group": {
            "_id": "$upvote",
            "count": { "$sum": 1 }
            }
        }, {
            '$sort': {
                'count': -1
            }
        }, {
            '$limit': 50
        }
    ])

    return '<pre>' + dumps(result, indent=2) + '</pre>'

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

    return '<pre>' + dumps(result, indent=2) + '</pre>'


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
    ])
    return '<pre>' + dumps(result,indent=2) + '</pre>'

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
        }, {
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

    return '<pre>' + dumps(result, indent=2) + '</pre>'
'''
@methods.route('/method11', methods=['GET'])
def getMethod11():
    result = mongo.db.log.aggregate([
        {
            '$match': {
                'blocks': {
                    '$ne': null
                }
            }
        },
        {
            '$lookup': {
                'from': 'admin',
                'let':{'log_id':'$log._id'},
                'pipeline': [ {
                                '$match': {
                                            '$expr': {
                                                        '$and':[ {'$in':['$$log_id','$upvotes'] },
                                                                 {'$eq' : ['$username','Brittany_Stevens'] }
                                                         ]
                                            } }
                                }
                ],
                'as': 'string'
            }
        }
        ,{
            '$match': {
                'string': {
                    '$ne': []
                }
            }
        }])

    mongo.db.admin.aggregate([
        {
            '$match': {
                'username': 'Brittany_Stevens'
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
                    '$ne': null
                }
            }
        }])
'''