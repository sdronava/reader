import uuid

def gen_id(prefix: str = "id") -> str:
    return f"{prefix}-{uuid.uuid4().hex}"
