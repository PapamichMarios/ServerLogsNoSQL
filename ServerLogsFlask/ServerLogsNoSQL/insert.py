from flask import Blueprint, request
from .extensions import mongo
from flask import jsonify
from datetime import datetime, tzinfo, timezone
from bson.json_util import dumps
from bson.objectid import ObjectId

from .logUtils import checkAccessLogEssential, checkDataLogEssential, checkLogEssential, checkDeleteLogEssential

insert = Blueprint('insert', __name__)

@insert.route('/insert/access', methods=['POST'])
def insertAccess():

    data = request.json

    #check for errors
    if not checkLogEssential(data)       : return '<h1>Not Accepted Log</h1>'
    if not checkAccessLogEssential(data) : return '<h1>Not Accepted Access Log</h1>'

    log = {}
    log['type']             = 'access'
    log['source_ip']        = data['source_ip']
    log['log_timestamp']    = datetime.strptime(data['log_timestamp'], "%Y-%m-%d %H:%M:%S")
    log['http_response']    = data['http_response']
    log['http_method']      = data['http_method']

    if 'user_id'        in data : log['user_id']      = data['user_id']
    if 'resource'       in data : log['resource']     = data['resource']
    if 'size'           in data : log['size']         = data['size']
    if 'referer'        in data : log['referer']      = data['referer']
    if 'agent_string'   in data : log['agent_string'] = data['agent_string']

    mongo.db.log.insert(log)
    return '<h1>Access Log Inserted!</h1>'

@insert.route('/insert/received', methods=['POST'])
def insertReceived():
    
    data = request.json

    #check for errors
    if not checkLogEssential(data)      : return '<h1>Not Accepted Log</h1>'
    if not checkDataLogEssential(data)  : return '<h1>Not Accepted Received Log</h1>'

    log = {}
    log['type']             = 'received'
    log['source_ip']        = data['source_ip']
    log['log_timestamp']    = datetime.strptime(data['log_timestamp'], "%Y-%m-%d %H:%M:%S")
    log['blocks']           = [data['blocks'][0]]
    log['destinations']     = [data['destinations'][0]]

    mongo.db.log.insert(log)
    return '<h1>Received Log Inserted</h1>'

@insert.route('/insert/receiving', methods=['POST'])
def insertReceiving():

    data = request.json

    #check for errors
    if not checkLogEssential(data)      : return '<h1>Not Accepted Log</h1>'
    if not checkDataLogEssential(data)  : return '<h1>Not Accepted Receiving Log</h1>'

    log = {}
    log['type']             = 'receiving'
    log['source_ip']        = data['source_ip']
    log['log_timestamp']    = datetime.strptime(data['log_timestamp'], "%Y-%m-%d %H:%M:%S")
    log['blocks']           = [data['blocks'][0]]
    log['destinations']     = [data['destinations'][0]]

    mongo.db.log.insert(log)
    return '<h1>Receiving Log Inserted</h1>'

@insert.route('/insert/served', methods=['POST'])
def insertServed():

    data = request.json

    #check for errors
    if not checkLogEssential(data)      : return '<h1>Not Accepted Log</h1>'
    if not checkDataLogEssential(data)  : return '<h1>Not Accepted Served Log</h1>'

    log = {}
    log['type']             = 'served'
    log['source_ip']        = data['source_ip']
    log['log_timestamp']    = datetime.strptime(data['log_timestamp'], "%Y-%m-%d %H:%M:%S")
    log['blocks']           = [data['blocks'][0]]
    log['destinations']     = [data['destinations'][0]]

    mongo.db.log.insert(log)
    return '<h1>Served Log Inserted</h1>'

@insert.route('/insert/replicate', methods=['POST'])
def insertReplicate():

    data = request.json

    #check for errors
    if not checkLogEssential(data)      : return '<h1>Not Accepted Log</h1>'
    if not checkDataLogEssential(data)  : return '<h1>Not Accepted Replicate Log</h1>'

    log = {}
    log['type']             = 'replicate'
    log['source_ip']        = data['source_ip']
    log['log_timestamp']    = datetime.strptime(data['log_timestamp'], "%Y-%m-%d %H:%M:%S")
    log['blocks']           = [data['blocks'][0]]
    log['destinations']     = data['destinations']

    mongo.db.log.insert(log)
    return '<h1>Replicate Log Inserted</h1>'

@insert.route('/insert/delete', methods=['POST'])
def insertDelete():
    
    data = request.json

    #check for errors
    if not checkLogEssential(data)       : return '<h1>Not Accepted Log</h1>'
    if not checkDeleteLogEssential(data) : return '<h1>Not Accepted Delete Log</h1>'

    log = {}
    log['type']             = 'delete'
    log['source_ip']        = data['source_ip']
    log['log_timestamp']    = datetime.strptime(data['log_timestamp'], "%Y-%m-%d %H:%M:%S")
    log['blocks']           = data['blocks']

    mongo.db.log.insert(log)
    return '<h1>Delete Log Inserted</h1>'


@insert.route('/insert/upvote', methods=['POST'])
def insertUpvote():
    data = request.json

    # check for errors
    '''
    if not checkLogEssential(data): return '<h1>Not Accepted Log</h1>'
    if not checkDeleteLogEssential(data): return '<h1>Not Accepted Delete Log</h1>'
    '''

    log = {}
    log['log_code'] = data['log_code']
    log['admin_code'] = data['admin_code']
    print(log['log_code'],log['admin_code'])
    results=mongo.db.admin.find({  '_id': ObjectId(log['admin_code']) ,
                         'upvotes': { '$elemMatch':
                                                { '$eq': ObjectId(log['log_code'])}
                                    }
                        }
                      )
    if len(list(results)):
        return '<h1>Upvote exists</h1>'
    else:
        upvote=mongo.db.admin.update(
            {"_id": ObjectId(log['admin_code'])},
            { '$push': {"upvotes" : ObjectId(log['log_code'])} }
        )
        return '<h1>Upvote Casted</h1>'

