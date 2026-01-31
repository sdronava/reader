from .ids import gen_id

def create_block(content: str, block_type: str = "text", metadata=None) -> dict:
    """Create a block dictionary for a piece of content"""
    return {
        "block_id": gen_id("blk"),
        "type": block_type,
        "content": content,
        "metadata": metadata or {},
        "tokens": len(content.split()),
    }
