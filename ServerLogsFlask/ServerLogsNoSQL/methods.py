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
    return 'Joey'
    
@methods.route('/method2', methods=['GET'])
def getMethod2():

    # get query params
    dayFrom = request.args.get('from')
    dayTo = request.args.get('to')
    logType = request.args.get('type')

    if not dayFrom or not dayTo or not logType:
        return 'Your url is not valid'

    logCollection = mongo.db.log
    result = logCollection.aggregate([
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
    return 'Joey'

@methods.route('/method4', methods=['GET'])
def getMethod4():
    
    # get query params
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
    return 'Joey'

@methods.route('/method6', methods=['GET'])
def getMethod6():
    
    logCollection = mongo.db.log
    result = logCollection.aggregate([
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
    
    return 'Joey'

@methods.route('/method8', methods=['GET'])
def getMethod8():
    
    logCollection = mongo.db.admin
    result = logCollection.aggregate([
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
    
    return 'Marios'

@methods.route('/method11', methods=['GET'])
def getMethod11():
    
    return 'Joey'
