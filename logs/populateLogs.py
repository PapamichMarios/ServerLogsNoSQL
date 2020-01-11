import json
import time
import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.log_db
batchSize = 500000

def monthToNum(shortMonth):
    return {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
    }[shortMonth]


def main():

    # parse access.log
    f = open("access.log", "r")
    lines = f.readlines()
    logs = []

    for line in lines: 
        words = line.split()
        for word in words[12:-1]:
            words[11]+=word

        agent = words[11][1:-1]
        ts = words[3][1:]
        stamp = ts[7:11] + "-" + monthToNum(ts[3:6]) + "-" + ts[0:2] + " " + ts[12:14] + ts[14:17] + ts[17:20]
        method = words[5][1:]

        if len(method) >= 10:
            continue

        log = {}
        log['type'] = "access"
        log['log_timestamp'] = datetime.datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S")
        log['source_ip'] = words[0]
        log['http_response'] = int(words[8])
        log['http_method'] = method
        
        if words[2]         != '-'  : log['user_id'] = words[2]
        if words[6]         != '-'  : log['resource'] = words[6]
        if words[9]         != '-'  : log['size'] = int(words[9])
        if words[10][1:-1]  != '-'  : log['referer'] = words[10][1:-1]
        if agent            != '-'  : log['agent_string'] = agent

        logs.append(log)

        if(len(logs) == batchSize):
            db.log.insert_many(logs)
            logs = []
        # print('id: ' + str(result.inserted_id))
        # time.sleep(5)

    f.close()
    if len(logs) > 0: db.log.insert_many(logs)
    
    #parse HDFS_DataXceiver.log
    f = open("HDFS_DataXceiver.log", "r")
    lines = f.readlines()
    logs = []

    for line in lines:
        words = line.split()

        ts = words[0] + words[1]
        stamp = "20"+ts[0:2]+"-"+ts[2:4]+"-"+ts[4:6]+" "+ts[6:8]+":"+ts[8:10]+":"+ts[10:12]

        log = {}
        log['log_timestamp'] = datetime.datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S")
        log['blocks'] = []
        log['destinations'] = []

        if (words[5] == "Received"):

            log['type'] = "received"  
            log['source_ip'] = words[9][1:]
            log['size'] = int(words[14])
            log['blocks'].append(words[7])
            log['destinations'].append(words[11][1:])
            logs.append(log)

        elif (words[5] == "Receiving"):

            log['type'] = "receiving"  
            log['source_ip'] = words[9][1:]
            log['blocks'].append(words[7])
            log['destinations'].append(words[11][1:])
            logs.append(log)

        elif (words[6] == "Served"):

            log['type'] = "served"  
            log['source_ip'] = words[5]
            log['blocks'].append(words[8])
            log['destinations'].append(words[10][1:])
            logs.append(log)

        if(len(logs) == batchSize):
            db.log.insert_many(logs)
            logs = []

    f.close()
    if len(logs) > 0: db.log.insert_many(logs)

    # HDFS_FS_Namesystem.log
    f = open("HDFS_FS_Namesystem.log", "r")
    lines = f.readlines()
    logs = []

    for line in lines:
        words = line.split()
        ts = words[0] + words[1]
        stamp = "20" + ts[0:2] + "-" + ts[2:4] + "-" + ts[4:6] + " " + ts[6:8] + ":" + ts[8:10] + ":" + ts[10:12]

        log = {}
        log['log_timestamp'] = datetime.datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S")
        log['blocks'] = []

        if (words[9] == "replicate"):

            log['type'] = "replicate"
            log['source_ip'] = words[7]
            log['blocks'].append(words[10])

            log['destinations'] = []
            for dest in words[13:]:
                log['destinations'].append(dest)
            
            logs.append(log)

        elif (words[9] == "delete"):
            
            log['type'] = "delete"
            log['source_ip'] = words[7]

            for block in words[10:]:
                log['blocks'].append(block)
            
            logs.append(log)

        if(len(logs) == batchSize):
            db.log.insert_many(logs)
            logs = []

    f.close()
    if len(logs) > 0: db.log.insert_many(logs)

if __name__ == "__main__":
    main()