import asyncio
import json
import base58
import os
import sys
import urllib.request
import nacl.signing
from indy_vdr import ledger, open_pool, LedgerType, VdrError, VdrErrorCode
from indy_vdr.error import VdrError
from indy_vdr.bindings import version
from indy_vdr.ledger import (
    LedgerType,
    build_custom_request,
    build_get_acceptance_mechanisms_request,
    build_get_cred_def_request,
    build_get_revoc_reg_def_request,
    build_get_revoc_reg_delta_request,
    build_get_revoc_reg_request,
    build_get_schema_request,
    build_node_request,
    build_pool_config_request,
    build_pool_restart_request,
    build_auth_rule_request,
    build_auth_rules_request,
    build_get_auth_rule_request,
    build_ledgers_freeze_request,
    build_get_frozen_ledgers_request,
    build_pool_upgrade_request,
    # build_revoc_reg_entry_request,
    # build_rich_schema_request,
    # build_get_schema_object_by_id_request,
    # build_get_schema_object_by_metadata_request,
    build_get_txn_author_agreement_request,
    build_get_txn_request,
    build_get_validator_info_request,
    prepare_txn_author_agreement_acceptance,
)
from indy_vdr.pool import Pool, open_pool
from indy_vdr.resolver import Resolver


def log(*args):
    print(*args, "\n")


async def get_pool_txns(pool: Pool):
    for txn in await pool.get_transactions():
        print(txn)


async def get_txn(pool: Pool, seq_no: int):
    req = build_get_txn_request(None, LedgerType.DOMAIN, seq_no)
    return await pool.submit_request(req)


async def get_txn_range(pool: Pool, seq_nos):
    return [await get_txn(pool, seq_no) for seq_no in seq_nos]

async def run_thread(fn, *args):
    return await asyncio.get_event_loop().run_in_executor(None, fn, *args)
async def get_validator_info(pool: Pool):  
    req = build_get_validator_info_request("V4SGRU86Z58d6TV7PBUe6f")
    return await pool.submit_action(req)
def seed_as_bytes(seed):
    if not seed or isinstance(seed, bytes):
        return seed
    if len(seed) != 32:
        return base64.b64decode(seed)
    return seed.encode("ascii")

def sign_request(self, req: ledger.Request, apply_taa: bool = True):
    if not self._did:
        raise AnchorException("Cannot sign request: no DID")
    if apply_taa and self._taa_accept:
        req.set_txn_author_agreement_acceptance(self._taa_accept)
    key = nacl.signing.SigningKey("000000000000000000000000Steward2")
    print("testing")
    signed = key.sign(req.signature_input)
    print(signed)
    req.set_signature(signed.signature)
    return req
async def submit_request(
    self, req: ledger.Request, signed: bool = False, apply_taa=False, as_action: bool = False
):
    try:
        if signed or (as_action and self.did):
            await run_thread(self.sign_request, req, apply_taa)
        if as_action:
            resp = await self._pool.submit_action(req)
        else:
            resp = await self._pool.submit_request(req)
    except VdrError as e:
        raise AnchorException("Error submitting ledger transaction request") from e

    return resp

async def get_nym(self, did: str):
    """
Fetch a nym from the ledger
"""
    if not self.ready:
        raise NotReadyException()

    get_nym_req = ledger.build_get_nym_request(self._did, did)
    response = await self.submit_request(get_nym_req, True)
    rv = {}

    data_json = response["data"]  # it's double-encoded on the ledger
    if data_json:
        rv = json.loads(data_json)
    return rv

# nymnym =  get_nym("Steward","EbP4aYNeTHL6q385GuVpRV")
# print("yoyoyoyoyoyoyoyoyoy")
# print(nymnym)
# print("yoyoyoyoyoyoyoyoyoy")

seed = "000000000000000000000000Steward2"
def nacl_seed_to_did(seed):
    seed = seed_as_bytes(seed)
    vk = bytes(nacl.signing.SigningKey(seed).verify_key)
    did = base58.b58encode(vk[:16]).decode("ascii")
    verkey = base58.b58encode(vk).decode("ascii")
    return did, verkey
asd = nacl_seed_to_did("000000000000000000000000Steward2")
print("below is the seed")
print(asd) # ('EbP4aYNeTHL6q385GuVpRV', '8QhFxKxyaFsJy4CyxeYX34dFH8oWqyBv1P4HLQCsoeLy')
print("above is the seed")
class AnchorException(Exception):
    pass
class NotReadyException(AnchorException):
    pass
async def get_nym(self, did: str):
    """
Fetch a nym from the ledger
"""
    if not self.ready:
        raise NotReadyException()

    get_nym_req = ledger.build_get_nym_request("000000000000000000000000Steward1", did)
    response = await self.submit_request(get_nym_req, True)
    rv = {}

    data_json = response["data"]  # it's double-encoded on the ledger
    if data_json:
        rv = json.loads(data_json)
    return rv

async def basic_test(transactions_path):
    pool = await open_pool(transactions_path=transactions_path)
    log("Created pool:", pool)

    verifiers = await pool.get_verifiers()
    log("Verifiers:", verifiers)

    #    req =  build_revoc_reg_entry_request(
    #     "CkTEG6qiypB8TCDS5mxRmy", "CkTEG6qiypB8TCDS5mxRmy:4:CkTEG6qiypB8TCDS5mxRmy:3:CL:67559:default:CL_ACCUM:e3abc098-749f-4c4a-a5f7-4e518035e820", "CL_ACCUM", '{"ver": "1.0", "value": {"accum": "21 117FA38C35FB5D721113285DC65741A227E860EA97195706A8EEEE778DE2A1013 21 137E20CCC0D5E63B79B1A392EBCC93A855EE6F80D95121A1F600F1FE11E5CB005 6 6D00C839527AE3B7E26B32A1AEACCA03A5415FF04A9ADA0D164E64E95AF7DAD0 4 02E046D5BBFC929582E79655B62FEEA65C86DC7EE1D6A7BE0A56E8BBF52FCCEB 6 70809B1DE08116FFDD5F91168EC5B87B2BD12E47A8952B2112A643500AB88D57 4 25AE5E9FEDC0BAC16FE765249B647ED69A5E73C5F956C34ADD0DAC5A4E4B2A95"}}')
    #     print(req)
    #     return

    test_req = {
        "operation": {"data": 1, "ledgerId": 1, "type": "3"},
        "protocolVersion": 2,
        "reqId": 123,
        "identifier": "EbP4aYNeTHL6q385GuVpRV",
    }
    req = build_custom_request(test_req)
    log("Custom request body:", req.body)
    #
    sig_in = req.signature_input
    log("Custom request signature input:", sig_in)

    req = build_get_txn_author_agreement_request()
    log(await pool.submit_request(req))

    req = build_get_acceptance_mechanisms_request()
    log(await pool.submit_request(req))

    acceptance = prepare_txn_author_agreement_acceptance(
        "acceptance text", "1.1.1", None, mechanism="manual"
    )
    req = build_get_txn_request(None, 1, 15)
    req.set_txn_author_agreement_acceptance(acceptance)
    req.set_endorser("EbP4aYNeTHL6q385GuVpRV")
    req.set_multi_signature("EbP4aYNeTHL6q385GuVpRV", b"sig")
    log("Request with TAA acceptance and endorser:", req.body)

    # req = build_disable_all_txn_author_agreements_request("V4SGRU86Z58d6TVis saif ali khan divorced7PBUe6f")
    # log(await pool.submit_request(req))

    txn = await get_txn(pool, 1)
    log(json.dumps(txn, indent=2))

    req = build_get_schema_request(
        None, "6qnvgJtqwK44D8LFYnV5Yf:2:relationship.dflow:1.0.0"
    )
    log("Get schema request:", req.body)

    req = build_get_cred_def_request(None, "A9Rsuu7FNquw8Ne2Smu5Nr:3:CL:15:tag")
    log("Get cred def request:", req.body)

    revoc_id = (
        "L5wx9FUxCDpFJEdFc23jcn:4:L5wx9FUxCDpFJEdFc23jcn:3:CL:1954:"
        "default:CL_ACCUM:c024e30d-f3eb-42c5-908a-ff885667588d"
    )

    req = build_get_revoc_reg_def_request(None, revoc_id)
    log("Get revoc reg def request:", req.body)

    req = build_get_revoc_reg_request(None, revoc_id, timestamp=1)
    log("Get revoc reg request:", req.body)

    req = build_get_revoc_reg_delta_request(None, revoc_id, from_ts=None, to_ts=1)
    log("Get revoc reg delta request:", req.body)

    identifier = "EbP4aYNeTHL6q385GuVpRV"
    dest = "EbP4aYNeTHL6q385GuVpRV"
    data = {
        "node_ip": "ip",
        "node_port": 1,
        "client_ip": "ip",
        "client_port": 1,
        "alias": "some",
        "services": ["VALIDATOR"],
        "blskey": "CnEDk9HrMnmiHXEV1WFgbVCRteYnPqsJwrTdcZaNhFVW",
    }
    req = build_node_request(identifier, dest, data)
    log("Node request:", req.body)

    req = build_pool_config_request(identifier, True, False)
    log("Pool Config request:", req.body)

    req = build_pool_restart_request(identifier, "start", None)
    log("Pool Restart request:", req.body)

    txn_type = "NYM"
    auth_type = "1"
    auth_action = "ADD"
    field = "role"
    old_value = "0"
    new_value = "101"
    constraint = {
        "sig_count": 1,
        "metadata": {},
        "role": "0",
        "constraint_id": "ROLE",
        "need_to_be_owner": False,
    }
    req = build_auth_rule_request(
        identifier, txn_type, auth_action, field, old_value, new_value, constraint
    )
    log("Auth Rule request:", req.body)

    rules = [
        {
            "auth_type": auth_type,
            "auth_action": auth_action,
            "field": field,
            "new_value": new_value,
            "constraint": constraint,
        },
    ]
    req = build_auth_rules_request(identifier, rules)
    log("Auth Rules request:", req.body)

    req = build_get_auth_rule_request(
        identifier, auth_type, auth_action, field, None, new_value
    )
    log("Get Auth Rule request:", req.body)

    ledgers_ids = [1, 10, 100]
    req = build_ledgers_freeze_request(identifier, ledgers_ids)
    log("Ledgers Freeze request:", req.body)

    req = build_get_frozen_ledgers_request(identifier)
    log("Get Frozen Ledgers request:", req.body)

    req = build_pool_upgrade_request(
        identifier, "up", "2.0.0", "start", "abc", None, {}, None, False, False, None
    )
    log("Pool Upgrade request:", req.body)

    # --- DID Resolution ---

    # The DID resolver can be initialized with a dict containing namespaces and pool instances:
    # pool_map = await open_pools(ledgers=["idunion", "sovrin:builder"])
    # resolver = Resolver(pool_map)

    # In addition, the the DID resolver can be started with autopilot = True.
    # Then it will try to fetch a genesis file from the did indy networks Github repo
    # for the given did:indy namespace.
    resolver = Resolver(autopilot=True)

    log("Resolve DID did:indy:idunion:test:APs6Xd2GH8FNwCaXDw6Qm2")
    doc = await resolver.resolve("did:indy:idunion:test:Fhbr2wQrJeB1UcZeFKpG5F")
    log(json.dumps(doc, indent=2))

    try:
        doc = await resolver.resolve("did:indy:idunion:test:APs6Xd2GH8FNwCaXDw6Qm2")
    except VdrError as err:
        print(err)

    # --- Rich Schema ---

    # req = build_rich_schema_request(
    #     None, "did:sov:some_hash", '{"some": 1}', "test", "version", "sch", "1.0.0"
    # )
    # log("Get rich schema request:", req.body)

    # req = build_get_schema_object_by_id_request(None, "did:sov:some_hash")
    # log("Get rich schema GET request by ID:", req.body)
    #
    # req = build_get_schema_object_by_metadata_request(None, "sch", "test", "1.0.0")
    # log("Get rich schema GET request by Metadata:", req.body)


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


def download_buildernet_genesis_file():
    genesis_file_url = (
        "https://raw.githubusercontent.com/wiredhikari/"
        "indy-sdk/main/genesis.txn"
    )
    target_local_path = f"{get_script_dir()}/genesis_sov_buildernet.txn"
    urllib.request.urlretrieve(genesis_file_url, target_local_path)
    return target_local_path


if __name__ == "__main__":
    log("indy-vdr  version:", version())

    genesis_path = (
        sys.argv[1] if len(sys.argv) > 1 else download_buildernet_genesis_file()
    )
    asyncio.get_event_loop().run_until_complete(basic_test(genesis_path))
