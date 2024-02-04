#!/usr/bin/python3

import asyncio
import logging
import os
import random
import sys
import traceback

import base58
import nacl.encoding
import nacl.signing
from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart import Quart, send_file
from indy_vdr.ledger import build_custom_request
from indy_vdr import ledger, pool

# NOTE: 0 Changes from 20 - 28
GENESIS_FILE = "/home/hikar/genesis.txn"

TRUSTEE_SEED = b"000000000000000000000000Steward2"
TRUSTEE_ID = "EbP4aYNeTHL6q385GuVpRV"
def key_to_did(key):
    key_bytes = bytes(key.verify_key)
    did = base58.b58encode(key_bytes[:16]).decode("ascii")
    verkey = "~" + base58.b58encode(key_bytes[16:]).decode("ascii")
    return did, verkey

"""
NOTE: Expected issue area...
    1. DIDDocument.authentication >>> originally it doesn't have feilds like "id", "type", "controller".... DOn't know if its required or not.
    2. Signature > sigbase64 === What is the Use?? 

NOTE: Question...
a. How this is derived???
>> "signature": {
                "verificationMethod": "did:exampleiin:org1#key1",
                "sigbase64": "sdfsdfsdf"
            }
        },
        "verkey": "~HFPBKb7S7ocrTzxakNbcao"
    },
    "protocolVersion": 2,
    "reqId": 1704282737760629997
"""



# @app.route('/create-did', methods=['POST'])
async def create_ou_did():
    global indy_pool
    print('Received OU-did request')
    indy_pool = await pool.open_pool(GENESIS_FILE)

    new_key = nacl.signing.SigningKey.generate()
    # keys.append(new_key)
    new_did, new_verkey = key_to_did(new_key)

    print(f"New DID: {new_did}")
    request_body="""
{
    "identifier": "EbP4aYNeTHL6q385GuVpRV",
    "operation": {
        "dest": "TWwCRQRZ2ZHMJFn9TzLp7W",
        "type": "77776",
        "data": { "DIDDocument": { "id": "did:exampleiin:org1","verificationMethod":[
                    {
                        "id": "did:exampleiin:org1#key1",
                        "type": "Ed25519VerificationKey2020",
                        "controller": "did:exampleiin:org1",
                        "publicKeyMultibase": "4PS3EDQ3dW1tci1Bp6543CfuuebjFrg36kLAUcskGfaA"
                    }
                ],
                "authentication": ["did:exampleiin:org1"] 
            },
            "signature": {
                "verificationMethod":[
                    {
                        "id": "did:exampleiin:org1#key1",
                        "type": "libnacl",
                        "controller": "did:exampleiin:org1",
                        "publicKeyMultibase": "4PS3EDQ3dW1tci1Bp6543CfuuebjFrg36kLAUcskGfaA"
                    }
                ],
                "sigbase64": "MG2bQ+yrRQ/ZbODDFdYL17XVkX2IZk2Y7ts34uvQceOB2R9zS0Yv47id3tXifzf6Vfm5YrnMRR+9eue+s67BAw=="  
            }
        },
        "verkey": "TWwCRQRZ2ZHMJFn9TzLp7W"
    },
    "protocolVersion": 2,
    "reqId": 1704282737760640010
}
"""
    req = ledger.build_custom_request( request_body )
    # print(req.body)
    key = nacl.signing.SigningKey(TRUSTEE_SEED)
    # author_signed = new_key.sign(req.signature_input)
    sig = key.sign(req.signature_input)

    req.set_signature(sig.signature)
    # req.set_multi_signature(new_did, author_signed.signature)
    print("hello")

    try:
        print("hello2.1")
        result = await indy_pool.submit_request(req)
        print(f"Response: {result}")
    except Exception as e:
    # try:
        print("hello2.2")
        print(f"Error: {e}: {traceback.format_exc()}")
asyncio.run(create_ou_did())

# async def update_did():create_did
#     global indy_pool
#     print('Received update-did request')
#     req = ledger.build_nym_request(
#         TRUSTEE_ID, TRUSTEE_ID, alias=random.choice(aliases))

#     key = nacl.signing.SigningKey(TRUSTEE_SEED)
#     sig = key.sign(req.signature_input)
#     req.set_signature(sig.signature)

#     await indy_pool.submit_request(req)
# asyncio.run(update())