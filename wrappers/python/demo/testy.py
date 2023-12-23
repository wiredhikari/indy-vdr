from nacl.signing import SigningKey
from nacl.signing import VerifyKey

# Generate a new random signing key
signing_key = SigningKey.generate()

# Sign a message with the signing key
signed = signing_key.sign(b"Attack at Dawn")

# Obtain the verify key for a given signing key
verify_key = signing_key.verify_key

# Serialize the verify key to send it to a third party
verify_key_bytes = verify_key.encode()



# Create a VerifyKey object from a hex serialized public key
verify_key = VerifyKey(verify_key_bytes)

# Check the validity of a message's signature
# The message and the signature can either be passed together, or
# separately if the signature is decoded to raw bytes.
# These are equivalent:
verify_key.verify(signed)
verify_key.verify(signed.message, signed.signature)

# Alter the signed message text
forged = signed[:-1] + bytes([int(signed[-1]) ^ 1])
# Will raise nacl.exceptions.BadSignatureError, since the signature check
# is failing
verify_key.verify(forged)