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

    new_key = nacl.signing.SigningKey.generate()
    print(new_key)
    # new_key = TRUSTEE_SEED
    # keys.append(new_key)
    new_did, new_verkey = key_to_did(new_key)

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
                "id": "did:exampleiin:org1",
                "verificationMethod": [
                    {
                        "id": "did:exampleiin:org1#key1",
                        "type": "libnacl",
                        "controller": "did:exampleiin:org1",
                        "publicKeyMultibase": "4PS3EDQ3dW1tci1Bp6543CfuuebjFrg36kLAUcskGfaA"
                    }
                ],
                "authentication": [
                    "did:exampleiin:org1"
                ]
            },
            "signature": {
                "verificationMethod": [
                    {
                        "id": "did:exampleiin:org1#key1",
                        "type": "libnacl",
                        "controller": "did:exampleiin:org1",
                        "publicKeyMultibase": "4PS3EDQ3dW1tci1Bp6543CfuuebjFrg36kLAUcskGfaA"
                    }
                ],
                "sigbase64": "Vz0xMYwovMPr6wyIBVoldel6N2jIh0Drn71+Pv5/5wARXZx6wvXr/jowFGam5dDodrShd/4WC0Ja64miC4KNCA=="
            }
        },
        "verkey": "TWwCRQRZ2ZHMJFn9TzLp7W"
    },
    "protocolVersion": 2,
    "reqId": 1704282737760640014
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
