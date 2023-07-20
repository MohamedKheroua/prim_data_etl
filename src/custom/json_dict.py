import json

def only_dict(d):
    '''
    Convert json string representation of dictionary to a python dict
    '''
    return json.loads(d)

def list_of_dicts(ld):
    '''
    Create a mapping of the tuples formed after 
    converting json strings of list to a python list   
    '''
    return dict([(list(d.values())[1], list(d.values())[0]) for d in json.loads(ld)])