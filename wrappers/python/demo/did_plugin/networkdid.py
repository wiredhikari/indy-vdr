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
async def create_sec_network_did():
    global indy_pool
    print('Received Security-Network DID request')
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
        "type": "33331",
        "data": {
            "DIDDocument": {
                "id": "did:iin:<iin_name>:<network_name>",
                "networkMembers": [
                    "did:iin:<iin_name>:<network_participant_1>",
                    "did:iin:<iin_name>:<network_participant_2>",
                    "did:iin:<iin_name>:<network_participant_3>"
                ],
                "verificationMethod": [
                    {
                        "id": "did:iin:<iin_name>:<network_name>#multisig",
                        "type": "BlockchainNetworkMultiSig",
                        "controller": "did:iin:<iin_name>:<network_name>",
                        "multisigKeys": [
                            "did:iin:<iin_name>:<network_participant_1>#key1",
                            "did:iin:<iin_name>:<network_participant_2>#key3",
                            "did:iin:<iin_name>:<network_participant_3>#key1"
                        ],
                        "updatePolicy": {
                            "id": "did:iin:<iin_name>:<network_name>#updatepolicy",
                            "controller": "did:iin:<iin_name>:<network_name>",
                            "type": "VerifiableCondition2021",
                            "conditionAnd": [
                                {
                                    "id": "did:iin:<iin_name>:<network_name>#updatepolicy-1",
                                    "controller": "did:iin:<iin_name>:<network_name>",
                                    "type": "VerifiableCondition2021",
                                    "conditionOr": [
                                        "did:iin:<iin_name>:<network_participant_3>#key1",
                                        "did:iin:<iin_name>:<network_participant_2>#key3"
                                    ]
                                },
                                "did:iin:<iin_name>:<network_participant_1>#key1"
                            ]
                        }
                    },
                    {
                        "id": "did:iin:<iin_name>:<network_name>#fabriccerts",
                        "type": "DataplaneCredentials",
                        "controller": "did:iin:<iin_name>:<network_name>",
                        "FabricCredentials": {
                            "did:iin:<iin_name>:<network_participant_1>": "Certificate3_Hash",
                            "did:iin:<iin_name>:<network_participant_2>": "Certificate2_Hash",
                            "did:iin:<iin_name>:<network_participant_3>": "Certificate3_Hash"
                        }
                    }
                ],
                "authentication": [
                    "did:iin:<iin_name>:<network_name>#multisig"
                ],
                "networkGatewayEndpoints": [
                    {
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
                "did:iin:<iin_name>:<network_participant_1>": "...",
                "did:iin:<iin_name>:<network_participant_2>": "...",
                "did:iin:<iin_name>:<network_participant_3>": "..."
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
asyncio.run(create_sec_network_did())
