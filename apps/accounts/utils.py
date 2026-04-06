import base64
import json


def decode_jwt_without_verification(token):
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid token format")

    payload_b64 = parts[1]
    padding = 4 - (len(payload_b64) % 4)
    if padding != 4:
        payload_b64 += "=" * padding

    payload_json = base64.urlsafe_b64decode(payload_b64)
    return json.loads(payload_json)
