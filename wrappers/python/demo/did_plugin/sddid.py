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
async def create_sd_did():
    global indy_pool
    print('Received SD-did request')
    indy_pool = await pool.open_pool(GENESIS_FILE)
    print("h1")
    new_key = nacl.signing.SigningKey.generate()
    # keys.append(new_key)
    new_did, new_verkey = key_to_did(new_key)

    print(f"New DID: {new_did}")
    request_body="""
{
    "identifier": "EbP4aYNeTHL6q385GuVpRV",
    "operation": {
        "dest": "TWwCRQRZ2ZHMJFn9TzLp7W",
        "type": "77777",
        "data": {
            "DIDDocument": { 
                "id": "did:iin_name:network_name",
                "networkMembers": [
                "did:iin_name:network_member_1",
                "did:iin_name:network_member_2",
                "did:iin_name:network_member_3"
                ],
                "verificationMethod": [{
                    "id": "did:iin_name:network_name#multisig",
                    "type": "BlockchainNetworkMultiSig",
                    "controller": "did:iin_name:network_name",
                    "multisigKeys": [
                        "did:iin_name:network_member_1#key1",
                        "did:iin_name:network_member_2#key3",
                        "did:iin_name:network_member_3#key1"
                    ],
                    "updatePolicy": {
                    "id": "did:iin_name:network_name#updatepolicy",
                    "controller": "did:iin_name:network_name",
                    "type": "VerifiableCondition2021",
                    "conditionAnd": [{
                        "id": "did:iin_name:network_name#updatepolicy-1",
                        "controller": "did:iin_name:network_name",
                        "type": "VerifiableCondition2021",
                        "conditionOr": ["did:iin_name:network_member_3#key1",
                            "did:iin_name:network_member_2#key3"
                        ]
                        },
                        "did:iin_name:network_member_1#key1"
                    ]
                    }
                },

                {
                    "id": "did:iin_name:network_name#fabriccerts",
                    "type": "DataplaneCredentials",
                    "controller": "did:iin_name:network_name",
                    "FabricCredentials": {
                    "did:iin_name:network_member_1": "Certificate1_Hash",
                    "did:iin_name:network_member_2": "Certificate2_Hash",
                    "did:iin_name:network_member_3": "Certificate3_Hash"
                    }
                }
                ],
                "authentication": [
                "did:iin_name:network_name#multisig"
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
                "did:iin_name:network_member_1": "BBCB75708867FD278D359E256FAD9AA3A85F02D64D2FB54C41DF081AA41B64D8087D6F94315CAF0C4A37179EBBF5650EB2ABE978ECDE8FBE6AF3646BE6A3D10D",
                "did:iin_name:network_member_2": "5895AAAAF1B320290962DB31D4C6F7930037F02835C5279C5F8F854D7AA5101ABA10CF136242CD744A1167B43294A7B49BA26F6C9BB9E8922123EF488CE4E703",
                "did:iin_name:network_member_3": "AE41AC9A626D93E5669C369E407AFCA006F28DD78F18635109B0249F9C2ABAF3F0453951A0CB41E41050D93BCD8CAA9CCE85A813CF12088CA38AA0F146227001"
            }
            },

        "verkey": "~HFPBKb7S7ocrTzxakNbcao"
    },
    "protocolVersion": 2,
    "reqId": 17042827377606
}
"""
    req = ledger.build_custom_request( request_body )
    # print(req.body)
    print("h2")
    key = nacl.signing.SigningKey(TRUSTEE_SEED)
    # author_signed = new_key.sign(req.signature_input)
    sig = key.sign(req.signature_input)
    print("h3")
    req.set_signature(sig.signature)
    # req.set_multi_signature(new_did, author_signed.signature)
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
asyncio.run(create_sd_did())

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
