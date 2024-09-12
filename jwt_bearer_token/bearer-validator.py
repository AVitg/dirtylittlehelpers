from __future__ import print_function
import base64
import json
import os.path
import pprint
import sys
import time
import zlib


def pad_base64(data):
    """Makes sure base64 data is padded
    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '='* (4 - missing_padding)
    return data


def decompress_partial(data):
    """Decompress arbitrary deflated data. Works even if header and footer is missing
    """
    decompressor = zlib.decompressobj()
    return decompressor.decompress(data)


def decompress(JWT):
    """Split a JWT to its constituent parts. 
    Decodes base64, decompress if required. Returns but does not validate the signature.
    """
    header, jwt, signature = JWT.split('.')

    printable_header = base64.urlsafe_b64decode(pad_base64(header)).decode('utf-8')

    if json.loads(printable_header).get("zip", "").upper() == "DEF":
        printable_jwt = decompress_partial(base64.urlsafe_b64decode(pad_base64(jwt)))
    else:
        printable_jwt = base64.urlsafe_b64decode(pad_base64(jwt)).decode('utf-8')

    printable_signature = base64.urlsafe_b64decode(pad_base64(signature))

    return json.loads(printable_header), json.loads(printable_jwt), printable_signature

    
def showJWT(JWT):
    header, jwt, signature = decompress(JWT)

    print("Header:  ", end="")
    pprint.pprint(header)

    print("Token:   ", end="")
    pprint.pprint(jwt)

    print("Issued at:  {} (localtime)".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(jwt['iat'])) if 'iat' in jwt else 'Undefined'))
    print("Not before: {} (localtime)".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(jwt['nbf'])) if 'nbf' in jwt else 'Undefined'))
    print("Expiration: {} (localtime)".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(jwt['exp'])) if 'exp' in jwt else 'Undefined'))

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         jwt = sys.argv[1]

#         if os.path.exists(jwt):
#             with open(sys.argv[1], "r") as input_file:
#                 jwt = input_file.read().strip()

#         showJWT(jwt)

if __name__ == "__main__":
    jwt=""
    showJWT(jwt)    