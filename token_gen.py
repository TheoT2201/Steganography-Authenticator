import hashlib
import base64
from datetime import datetime, timezone

def generate_token(username, password):
    current_time = datetime.now(timezone.utc).isoformat()
    token_string = f"{username}:{password}:{current_time}"

    print(current_time)

    hash_object = hashlib.sha256(token_string.encode())
    hashed_token = hash_object.digest()

    encoded_token = base64.b64encode(hashed_token).decode()
    
    return encoded_token