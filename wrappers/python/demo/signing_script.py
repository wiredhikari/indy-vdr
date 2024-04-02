from nacl.signing import SigningKey
from nacl.encoding import HexEncoder, Base64Encoder
import json

# Mock private key for demonstration; in real use, a valid Ed25519 private key should be provided.
# The provided private key is not in a valid format, so we're using a placeholder for demonstration.
mock_private_key_hex = "5FC32A64AAD3E3CE5AE1979F006C65518F02DFE4CE45EEF3809DEEAE7786C501"  # A 32-byte (64 characters in hexadecimal) mock private key.
print(mock_private_key_hex)
# Decode the mock private key from hexadecimal.
private_key = SigningKey(mock_private_key_hex, encoder=HexEncoder)

# The JSON object to be signed.
json_object = {
                "authentication": [
                    "did:iin_name:network_member_1"
                ],
                "id": "did:exampleiin:network_member_1",
                "verificationMethod": [
                    {
                        "id": "did:iin_name:network_member_1#key1",
                        "type": "libnacl",
                        "controller": "did:iin_name:network_member_1",
                        "publicKeyMultibase": "D3C2E00FEA8E0E9A005CF2D2863B52F3FBE3657088593DB8E3B9EA8E88609861"
                    }
                ]
            
}

# Convert the JSON object to a string and then to bytes.
json_bytes = json.dumps(json_object).encode('utf-8')
print(json_bytes)

# Sign the JSON bytes.
signature = private_key.sign(json_bytes)

# Encode the signature in Base64 to make it easy to share or store.
signature_base64 = Base64Encoder.encode(signature.signature).decode('utf-8')

print(signature_base64)
