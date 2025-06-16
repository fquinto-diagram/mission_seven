import base64


def decode_to_base64(data: str) -> str:
    return base64.b64decode(data).decode('utf-8')