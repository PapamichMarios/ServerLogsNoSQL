def checkLogEssential(data):
    if 'source_ip' in data and 'log_timestamp' in data:
        return True

    return False

def checkAccessLogEssential(data):
    if 'http_response' in data and 'http_method' in data:
        return True

    return False

def checkDataLogEssential(data):
    if 'blocks' in data and 'destinations' in data:
        if len(data['blocks'])>0 and len(data['destinations'])>0:
            return True

    return False

def checkDeleteLogEssential(data):
    if 'blocks' in data:
        return True
        
    return False