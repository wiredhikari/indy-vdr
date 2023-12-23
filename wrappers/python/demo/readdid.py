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
TRUSTEE_ID = "EbP4aYNeTHL6q385GuVpRV"

async def read_did():

    GENESIS_FILE = "/home/hikar/genesis.txn"
    indy_pool = await pool.open_pool(GENESIS_FILE)
    # global indy_pool
    #logger.info('Received read-did request')
    get_req = ledger.build_get_nym_request(None, TRUSTEE_ID)
    result = await indy_pool.submit_request(get_req)
    print(result)
    print("as")
asyncio.run(read_did())
#    logger.info(f"Read DID: {result}\n")
    # return "Read DID!"
# read_did()
# aliases = ["Alice", "Bob", "Charlie", "Dean", "Eric"]
