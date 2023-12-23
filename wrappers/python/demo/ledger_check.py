#!/usr/bin/python3

import asyncio
import pprint

from indy_vdr import ledger, pool

# import indy_vdr

path = "/home/hikar/genesis.txn"
TRUSTEE_SEED = b"000000000000000000000000Steward2"
TRUSTEE_ID = "EbP4aYNeTHL6q385GuVpRV"

async def check():
    req = ledger.build_get_txn_request(None, 1, 1)
    my_pool = await pool.open_pool(path)

    first_txn = await my_pool.submit_request(req)
    print("First txn: ")
    pprint.pprint(first_txn['data']['txn'])

    ledger_size = first_txn['data']['ledgerSize']

    req = ledger.build_get_txn_request(None, 1, ledger_size)

    last_txn = await my_pool.submit_request(req)

    print("Last txn: ")
    pprint.pprint(last_txn['data']['txn'])

    print(f"Ledger size: {ledger_size}")

if __name__ == "__main__":
    asyncio.run(check())
