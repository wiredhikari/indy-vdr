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


GENESIS_FILE = "/home/hikar/genesis.txn"

TRUSTEE_SEED = b"000000000000000000000000Steward2"
TRUSTEE_ID = "EbP4aYNeTHL6q385GuVpRV"
def key_to_did(key):
    key_bytes = bytes(key.verify_key)
    did = base58.b58encode(key_bytes[:16]).decode("ascii")
    verkey = "~" + base58.b58encode(key_bytes[16:]).decode("ascii")
    return did, verkey


# @app.route('/create-did', methods=['POST'])
async def create_did():
    global indy_pool
    print('Received create-did request')
    indy_pool = await pool.open_pool(GENESIS_FILE)

    new_key = nacl.signing.SigningKey.generate()
    # keys.append(new_key)
    new_did, new_verkey = key_to_did(new_key)

    print(f"New DID: {new_did}")
    request_body="""
{
    "identifier": "EbP4aYNeTHL6q385GuVpRV",
    "operation": {
        "dest": "Vzfdscz6YG6n1EuNJV4ob1",
        "type": "20220",
        "data": {
            "DIDDocument": {
                "@context": [
                    "https://www.w3.org/ns/did/v1",
                    "https://w3id.org/security/suites/ed25519-2020/v1"
                ],
                "id": "did:iin:iin123:shippingcompany",
                "verificationMethod": [
                    {
                        "id": "did:iin:iin123:shippingcompany#key-1",
                        "type": "Ed25519VerificationKey2020",
                        "controller": "did:example:123456789abcdefghi",
                        "publicKeyBase64": "zH3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
                    }
                ],
                "authentication": [
                    "did:iin:iin123:shippingcompany#keys-1",
                    {
                        "id": "did:iin:iin123:shippingcompany#keys-2",
                        "type": "Ed25519VerificationKey2020",
                        "controller": "did:shippingcompany",
                        "publicKeyBase64": "zH3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
                    }
                ]
            },
            "signature": {
                "verificationMethod": "did:iin:iin123:shippingcompany#keys-1",
                "sigbase64": "sdfsdfsdf"
            }
        },
        "verkey": "~HFPBKb7S7ocrTzxakNbcao"
    },
    "protocolVersion": 2,
    "reqId": 1704282737760629997
}
"""
    req = ledger.build_custom_request( request_body )
    # print(req.body)
    key = nacl.signing.SigningKey(TRUSTEE_SEED)
    # author_signed = new_key.sign(req.signature_input)
    sig = key.sign(req.signature_input)

    req.set_signature(sig.signature)
    # req.set_multi_signature(new_did, author_signed.signature)
    

    try:
        result = await indy_pool.submit_request(req)
        print(f"Response: {result}")
    except Exception as e:
    # try:
        print(f"Error: {e}: {traceback.format_exc()}")
asyncio.run(create_did())

# async def update_did():
#     global indy_pool
#     print('Received update-did request')
#     req = ledger.build_nym_request(
#         TRUSTEE_ID, TRUSTEE_ID, alias=random.choice(aliases))

#     key = nacl.signing.SigningKey(TRUSTEE_SEED)
#     sig = key.sign(req.signature_input)
#     req.set_signature(sig.signature)

#     await indy_pool.submit_request(req)
# asyncio.run(update())
