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

    return dumps(result)

@methods.route('/method3', methods=['GET'])
def getMethod3():
    logCollection = mongo.db.log
    result = logCollection.aggregate(
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

    return dumps(result)

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

    return dumps(result)


@methods.route('/method7', methods=['GET'])
def getMethod7():
    logCollection = mongo.db.admin
    result = logCollection.aggregate([
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

    return dumps(result)


@methods.route('/method9', methods=['GET'])
def getMethod9():
    
    return 'Joey'

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

    return dumps(result)

@methods.route('/method11', methods=['GET'])
def getMethod11():
    
    return 'Joey'
