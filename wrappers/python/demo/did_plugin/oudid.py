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
    # key = TRUSTEE_SEED
    key_bytes = bytes(key.verify_key)
    did = base58.b58encode(key_bytes[:16]).decode("ascii")
    verkey = "~" + base58.b58encode(key_bytes[16:]).decode("ascii")
    print (f"did::>> {did} ||| verkey::>> {verkey}")
    return did, verkey

# @app.route('/create-did', methods=['POST'])
async def create_ou_did():
    global indy_pool
    print('Received OU-did request')
    indy_pool = await pool.open_pool(GENESIS_FILE)

    new_key = nacl.signing.SigningKey(b'\xa5i\x95\xcc\xf0cB\\\x8b\x86U\x02\xcaR\xf1?\xcd?\x89\xdf\xfa\xa9\xe6s"\xfd?V\x1dS\x00\xd8')
    print(new_key)
    # new_key = TRUSTEE_SEED
    # keys.append(new_key)
    new_did, new_verkey = key_to_did(new_key)
    print(new_verkey)

# zH3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV
# 4PS3EDQ3dW1tci1Bp6543CfuuebjFrg36kLAUcskGfaA   XXXXX

    print(f"New DID: {new_did}")
    request_body="""
{
    "identifier": "EbP4aYNeTHL6q385GuVpRV",
    "operation": {
        "dest": "TWwCRQRZ2ZHMJFn9TzLp7W",
        "type": "77776",
        "data": {
            "DIDDocument": {
                "authentication": [
                    "did:iin_name:network_member_1"
                ],
                "id": "did:exampleiin:network_member_1",
                "verificationMethod": [
                    {
                        "id": "did:iin_name:network_member_1#key1",
                        "type": "libnacl",
                        "controller": "did:iin_name:network_member_1",
                        "publicKeyMultibase": "NUJMMnZHWEFqdFMzcmRmUjJtVmRwVw=="
                    }
                ]
            },
            "signature": {
                "verificationMethod": [
                    {
                        "id": "did:iin_name:network_member_1#8D18B4FB4F0AE4AC00C0F63EA2C719C06AB597CE34C8306D1810146D51126EE4",
                        "type": "libnacl",
                        "controller": "did:iin_name:network_member_1",
                        "publicKeyMultibase": "NUJMMnZHWEFqdFMzcmRmUjJtVmRwVw=="
                    }
                ],
                "sigbase64": "fz9zxRvgqqZMrRXFz2HJyBVJwaC9acB9OwzitGqOT9XsTH7vgnDZRwlQxUCPEvo+nJNgV/8BNDjzOAj9w6r7Aw=="
            }
        },
        "verkey": "5BL2vGXAjtS3rdfR2mVdpW"
    },
    "protocolVersion": 2,
    "reqId": 1704282737760640014
}
"""
#~5BL2vGXAjtS3rdfR2mVdpW
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


"""
The 3 oudids

OUDID 1 
{
    "identifier": "EbP4aYNeTHL6q385GuVpRV",
    "operation": {
        "dest": "TWwCRQRZ2ZHMJFn9TzLp7W",
        "type": "77776",
        "data": {
            "DIDDocument": {
                "authentication": [
                    "did:iin_name:network_member_1"
                ],
                "id": "did:exampleiin:network_member_1",
                "verificationMethod": [
                    {
                        "id": "did:iin_name:network_member_1#8D18B4FB4F0AE4AC00C0F63EA2C719C06AB597CE34C8306D1810146D51126EE4",
                        "type": "libnacl",
                        "controller": "did:iin_name:network_member_1",
                        "publicKeyMultibase": "mOEQxOEI0RkI0RjBBRTRBQzAwQzBGNjNFQTJDNzE5QzA2QUI1OTdDRTM0QzgzMDZEMTgxMDE0NkQ1MTEyNkVFNA"
                    }
                ]
            },
            "signature": {
                "verificationMethod": [
                    {
                        "id": "did:iin_name:network_member_1#key1",
                        "type": "libnacl",
                        "controller": "did:iin_name:network_member_1",
                        "publicKeyMultibase": "mOEQxOEI0RkI0RjBBRTRBQzAwQzBGNjNFQTJDNzE5QzA2QUI1OTdDRTM0QzgzMDZEMTgxMDE0NkQ1MTEyNkVFNA"
                    }
                ],
                "sigbase64": "fz9zxRvgqqZMrRXFz2HJfz9zxRvgqqZMrRXFz2HJyBVJwaC9acB9OwzitGqOT9XsTH7vgnDZRwlQxUCPEvoyBVJwaC9acB9OwzitGqOT9XsTH7vgnDZRwlQxUCPEvo+nJNgV/8BNDjzOAj9w6r7Aw=="
            }
        },
        "verkey": "5BL2vGXAjtS3rdfR2mVdpW"
    },
    "protocolVersion": 2,
    "reqId": 1704282737760640014
}

OUDID 2
{
    "identifier": "EbP4aYNeTHL6q385GuVpRV",
    "operation": {
        "dest": "TWwCRQRZ2ZHMJFn9TzLp7W",
        "type": "77776",
        "data": {
            "DIDDocument": {
                "authentication": [
                    "did:iin_name:network_member_2"
                ],
                "id": "did:exampleiin:network_member_2",
                "verificationMethod": [
                    {
                        "id": "did:iin_name:network_member_2#key2",
                        "type": "libnacl",
                        "controller": "did:iin_name:network_member_1",
                        "publicKeyMultibase": "mQzlCNzE2QzQyQjJDMjZCQzY2MkYxQUZDRUNBMEUyNjlFMTU1NUM5MTZGQTY4RkY0OUY0Rjg3RDc0OTVERENGRA"
                    }
                ]
            },
            "signature": {
                "verificationMethod": [
                    {
                        "id": "did:iin_name:network_member_1#key2",
                        "type": "libnacl",
                        "controller": "did:iin_name:network_member_2",
                        "publicKeyMultibase": "mQzlCNzE2QzQyQjJDMjZCQzY2MkYxQUZDRUNBMEUyNjlFMTU1NUM5MTZGQTY4RkY0OUY0Rjg3RDc0OTVERENGRA"
                    }
                ],
                "sigbase64": "C82B305CF7062C6269AAE6747A4B6561D6E9E985F2418128ED38D12A2E739049192A786A7B573E3B9148F43A6D2A091F9029A02ACF102FE5E2B8385AB550EC04"
            }
        },
        "verkey": "5BL2vGXAjtS3rdfR2mVdpW"
    },
    "protocolVersion": 2,
    "reqId": 1704282737760640014
}

OUDID 3
{
    "identifier": "EbP4aYNeTHL6q385GuVpRV",
    "operation": {
        "dest": "TWwCRQRZ2ZHMJFn9TzLp7W",
        "type": "77776",
        "data": {
            "DIDDocument": {
                "authentication": [
                    "did:iin_name:network_member_3"
                ],
                "id": "did:exampleiin:network_member_3",
                "verificationMethod": [
                    {
                        "id": "did:iin_name:network_member_3#key1",
                        "type": "libnacl",
                        "controller": "did:iin_name:network_member_3",
                        "publicKeyMultibase": "mOEQxOEI0RkI0RjBBRTRBQzAwQzBGNjNFQTJDNzE5QzA2QUI1OTdDRTM0QzgzMDZEMTgxMDE0NkQ1MTEyNkVFNA"
                    }
                ]
            },
            "signature": {
                "verificationMethod": [
                    {
                        "id": "did:iin_name:network_member_3#key1",
                        "type": "libnacl",
                        "controller": "did:iin_name:network_member_3",
                        "publicKeyMultibase": "mOEQxOEI0RkI0RjBBRTRBQzAwQzBGNjNFQTJDNzE5QzA2QUI1OTdDRTM0QzgzMDZEMTgxMDE0NkQ1MTEyNkVFNA"
                    }
                ],
                "sigbase64": "fz9zxRvgqqZMrRXFz2HJyBVJwaC9acB9OwzitGqOT9XsTH7vgnDZRwlQxUCPEvo+nJNgV/8BNDjzOAj9w6r7Aw=="
            }
        },
        "verkey": "5BL2vGXAjtS3rdfR2mVdpW"
    },
    "protocolVersion": 2,
    "reqId": 1704282737760640014
}


"""