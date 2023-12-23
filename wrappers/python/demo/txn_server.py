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

from indy_vdr import ledger, pool

logger = logging.getLogger(__name__)

app = Quart(__name__)

GENESIS_FILE = "/home/hikar/genesis.txn"

TRUSTEE_SEED = b"000000000000000000000000Steward2"
TRUSTEE_ID = "EbP4aYNeTHL6q385GuVpRV"

global keys
keys = []


def key_to_did(key):
    key_bytes = bytes(key.verify_key)
    did = base58.b58encode(key_bytes[:16]).decode("ascii")
    verkey = "~" + base58.b58encode(key_bytes[16:]).decode("ascii")
    return did, verkey


@app.route('/create-did', methods=['POST'])
async def create_did():
    global indy_pool
    logger.info('Received create-did request')

    new_key = nacl.signing.SigningKey.generate()
    keys.append(new_key)
    new_did, new_verkey = key_to_did(new_key)

    logger.info(f"New DID: {new_did}")

    req = ledger.build_nym_request(
        TRUSTEE_ID, new_did, verkey=new_verkey, role=None)

    key = nacl.signing.SigningKey(TRUSTEE_SEED)
#    author_signed = new_key.sign(req.signature_input)
    sig = key.sign(req.signature_input)

    req.set_signature(sig.signature)
#    req.set_multi_signature(new_did, author_signed.signature)

    while True:
        try:
            result = await indy_pool.submit_request(req)
            logger.info(f"Response: {result}")
            break
        except Exception as e:
            logger.error(f"Error: {e}: {traceback.format_exc()}")
    return 'Created DID!\n'


@app.route('/read-did', methods=['GET'])
async def read_did():
    global indy_pool
    logger.info('Received read-did request')
    get_req = ledger.build_get_nym_request(None, TRUSTEE_ID)
    result = await indy_pool.submit_request(get_req)

#    logger.info(f"Read DID: {result}\n")
    return "Read DID!"

aliases = ["Alice", "Bob", "Charlie", "Dean", "Eric"]


@app.route('/update-did', methods=['POST'])
async def update_did():
    global indy_pool
    logger.info('Received update-did request')
    req = ledger.build_nym_request(
        TRUSTEE_ID, TRUSTEE_ID, alias=random.choice(aliases))

    key = nacl.signing.SigningKey(TRUSTEE_SEED)
    sig = key.sign(req.signature_input)
    req.set_signature(sig.signature)

    await indy_pool.submit_request(req)
    return 'Updated DID!\n'

async def setup():
    global indy_pool
    with open(GENESIS_FILE, 'r') as file:
        for line in file:
            logger.info(line)

    indy_pool = await pool.open_pool(GENESIS_FILE)

if __name__ == "__main__":
    asyncio.run(setup())
    server_port = sys.argv[1] if len(sys.argv) > 1 else "5555"

    logFilename = "logs/txns." + server_port + ".log"

    os.makedirs(os.path.dirname(logFilename), exist_ok=True)

    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(logFilename, mode='w')
    # fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    logger.addHandler(sh)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

#     port_int = int(server_port)
#     app.run(host='0.0.0.0', debug=True, port=port_int)

    config = Config()
    config.bind = ["localhost:" + server_port]
    asyncio.run(serve(app, config))
