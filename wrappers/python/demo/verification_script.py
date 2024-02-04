import libnacl
import libnacl.encode

def libnacl_validate(vk_base64, signature_base64, originalhash):
    print("hello1")
    vk = libnacl.encode.base64_decode(vk_base64)
    print("hello2", vk)
    signature = libnacl.encode.base64_decode(signature_base64)
    print("hello3", signature)
    verifiedhash = libnacl.crypto_sign_open(signature, vk)
    print("hello4",verifiedhash)
    print("VERIFIED_HASH", verifiedhash)
    if verifiedhash != originalhash:
        print("The hash of the DIDDocument did not match.")


# Provided values
vk_base64 = '4PS3EDQ3dW1tci1Bp6543CfuuebjFrg36kLAUcskGfaA'
signature_base64 = "MG2bQ+yrRQ/ZbODDFdYL17XVkX2IZk2Y7ts34uvQceOB2R9zS0Yv47id3tXifzf6Vfm5YrnMRR+9eue+s67BAw=="
originalhash = b'\xdfC\xa4\xdf\xb3\xbd^\xde\xdf\xf8\t\xda\x14l\x88\xe9V\xd0\xd0\x19QI\xad\x89\xfdI\xd9\xd6\xe0rA\x94'

# Call the function with the provided values
verification_result = libnacl_validate(vk_base64, signature_base64, originalhash)

verification_result
