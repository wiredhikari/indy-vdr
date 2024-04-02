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
vk_base64 = 'NUJMMnZHWEFqdFMzcmRmUjJtVmRwVw=='
signature_base64 = "fz9zxRvgqqZMrRXFz2HJyBVJwaC9acB9OwzitGqOT9XsTH7vgnDZRwlQxUCPEvo+nJNgV/8BNDjzOAj9w6r7Aw=="
originalhash = b'\xa5i\x95\xcc\xf0cB\\\x8b\x86U\x02\xcaR\xf1?\xcd?\x89\xdf\xfa\xa9\xe6s"\xfd?V\x1dS\x00\xd8'

# Call the function with the provided values
verification_result = libnacl_validate(vk_base64, signature_base64, originalhash)

verification_result
