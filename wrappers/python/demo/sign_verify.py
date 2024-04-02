import json
import libnacl
import libnacl.encode

def libnacl_validate2( vk_base64, signature_base64, originalhash):
    print("vk_base64", vk_base64)
    print("signature_base64", signature_base64)
    vk = libnacl.encode.base64_decode(vk_base64)
    signature = libnacl.encode.base64_decode(signature_base64)
    verifiedhash = libnacl.crypto_sign_open(signature, vk)
    if verifiedhash != originalhash:
        print("The hash of the DIDDocument did not match.")

originalhash = libnacl.crypto_hash_sha256(self.did_str)
libnacl_validate2("", "", originalhash)