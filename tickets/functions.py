import hashlib


def sign_validation_request(track_code, ticket_id, ticket_signature, validator_id, secret_key):
    key = '%s%s%s%s%s' % (track_code, ticket_id, ticket_signature, validator_id, secret_key)
    sha1 = hashlib.sha1(key.encode('utf-8'))
    return sha1.hexdigest().upper()
