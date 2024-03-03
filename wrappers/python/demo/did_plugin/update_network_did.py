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

# @app.route('/create-did', methods=['POST'])

async def update_network_did():
    global indy_pool
    print('Received Update-network-did request')

    indy_pool = await pool.open_pool(GENESIS_FILE)
    print("h1")
    new_key = nacl.signing.SigningKey.generate()
    new_did, new_verkey = key_to_did(new_key)

    print(f"New DID: {new_did}")
    request_body="""
{
    "identifier": "EbP4aYNeTHL6q385GuVpRV",
    "operation": {
        "dest": "TWwCRQRZ2ZHMJFn9TzLp7W",
        "type": "77774",
        "data": {
            "DIDDocument": {
                "id": "did:<iin_name>:<network_name>",
                "networkMembers": [
                "did:<iin_name>:<network_member_1>",
                "did:<iin_name>:<network_member_2>",
                "did:<iin_name>:<network_member_3>"
                ],
                "verificationMethod": [{
                    "id": "did:<iin_name>:<network_name>#multisig",
                    "type": "BlockchainNetworkMultiSig",
                    "controller": "did:<iin_name>:<network_name>",
                    "multisigKeys": [
                    "did:<iin_name>:<network_member_1>#key1",
                    "did:<iin_name>:<network_member_2>#key3",
                    "did:<iin_name>:<network_member_3>#key1"
                    ],
                    "updatePolicy": {
                    "id": "did:<iin_name>:<network_name>#updatepolicy",
                    "controller": "did:<iin_name>:<network_name>",
                    "type": "VerifiableCondition2021",
                    "conditionAnd": [{
                        "id": "did:<iin_name>:<network_name>#updatepolicy-1",
                        "controller": "did:<iin_name>:<network_name>",
                        "type": "VerifiableCondition2021",
                        "conditionOr": ["did:<iin_name>:<network_member_3>#key1",
                            "did:<iin_name>:<network_member_2>#key3"
                        ]
                        },
                        "did:<iin_name>:<network_member_1>#key1"
                    ]
                    }
                },

                {
                    "id": "did:<iin_name>:<network_name>#fabriccerts",
                    "type": "DataplaneCredentials",
                    "controller": "did:<iin_name>:<network_name>",
                    "FabricCredentials": {
                    "did:<iin_name>:<network_member_1>": "Certificate3_Hash",
                    "did:<iin_name>:<network_member_2>": "Certificate2_Hash",
                    "did:<iin_name>:<network_member_3>": "Certificate3_Hash"
                    }
                }
                ],
                "authentication": [
                "did:<iin_name>:<network_name>#multisig"
                ],
                "relayEndpoints": [{
                    "hostname": "10.0.0.8",
                    "port": "8888"
                },
                {
                    "hostname": "10.0.0.9",
                    "port": "8888"
                }

                ]
            },
            "signatures": {
                "did:<iin_name>:<network_member_1>": "...",
                "did:<iin_name>:<network_member_2>": "...",
                "did:<iin_name>:<network_member_3>": "..."
            }
            },

        "verkey": "~HFPBKb7S7ocrTzxakNbcao"
    },
    "protocolVersion": 2,
    "reqId": 1704282737760649997
}
"""
    req = ledger.build_custom_request( request_body )
    
    print("h2")
    key = nacl.signing.SigningKey(TRUSTEE_SEED)
    sig = key.sign(req.signature_input)
    print("h3")
    req.set_signature(sig.signature)
    print("h4")

    try:
        print("h5")
        result = await indy_pool.submit_request(req)
        print(f"Response: {result}")
        print("h6")

    except Exception as e:
    # try:
        print("h7")
        print(f"Error: {e}: {traceback.format_exc()}")
asyncio.run(update_network_did())
