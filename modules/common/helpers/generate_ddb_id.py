from hashlib import sha1
from base64 import b32encode

def get_ddb_id(provider_id, origin_id):

    hash_source_string = "{}{}".format(provider_id, origin_id)
    ddb_id = b32encode(sha1(hash_source_string.encode('utf-8')).digest())

    return ddb_id.decode('utf-8')
