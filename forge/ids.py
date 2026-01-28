import uuid

def gen_id(prefix: str) -> str:
    """
    Generate a short unique ID with a prefix.
    Example: blk-1a2b3c4d
    """
    return f"{prefix}-{str(uuid.uuid4())[:8]}"