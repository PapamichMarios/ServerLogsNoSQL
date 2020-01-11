from flask import Blueprint, request
from .extensions import mongo
from flask import jsonify
from datetime import datetime, tzinfo, timezone
from bson.json_util import dumps

insert = Blueprint('insert', __name__)

@insert.route('/insert/access', methods=['POST'])
def insertAccess():
    return '<h1>Access</h1>'

@insert.route('/insert/received', methods=['POST'])
def insertReceived():
    return '<h1>Received</h1>'

@insert.route('/insert/receiving', methods=['POST'])
def insertReceiving():
    return '<h1>Receiving</h1>'

@insert.route('/insert/served', methods=['POST'])
def insertServed():
    return '<h1>Served</h1>'

@insert.route('/insert/replicate', methods=['POST'])
def insertReplicate():
    return '<h1>Replicate</h1>'

@insert.route('/insert/delete', methods=['POST'])
def insertDelete():
    return '<h1>Delete</h1>'