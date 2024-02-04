from nacl.signing import SigningKey
from nacl.encoding import HexEncoder, Base64Encoder
import json

# Mock private key for demonstration; in real use, a valid Ed25519 private key should be provided.
# The provided private key is not in a valid format, so we're using a placeholder for demonstration.
mock_private_key_hex = "a" * 64  # A 32-byte (64 characters in hexadecimal) mock private key.

# Decode the mock private key from hexadecimal.
private_key = SigningKey(mock_private_key_hex, encoder=HexEncoder)

# The JSON object to be signed.
json_object = {
    "id": "did:exampleiin:org1",
    "verificationMethod": [
        {
            "id": "did:exampleiin:org1#key1",
            "type": "libnacl",
            "controller": "did:exampleiin:org1",
            "publicKeyMultibase": "4PS3EDQ3dW1tci1Bp6543CfuuebjFrg36kLAUcskGfaA"
        }
    ],
    "authentication": [
        "did:exampleiin:org1"
    ]
}

# Convert the JSON object to a string and then to bytes.
json_bytes = json.dumps(json_object, separators=(',', ':')).encode('utf-8')

# Sign the JSON bytes.
signature = private_key.sign(json_bytes)

# Encode the signature in Base64 to make it easy to share or store.
signature_base64 = Base64Encoder.encode(signature.signature).decode('utf-8')

print(signature_base64)
