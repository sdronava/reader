from .ids import gen_id

def create_block(
    content: str,
    block_type: str = "text",
    metadata: dict | None = None,
    tokens: int | None = None,
) -> dict:
    """
    Create a block dictionary for a piece of content.
    """
    return {
        "block_id": gen_id("blk"),
        "type": block_type,
        "content": content,
        "metadata": metadata or {},
        "tokens": tokens if tokens is not None else len(content.split()),
    }