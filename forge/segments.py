from .ids import gen_id

MAX_BLOCKS = 10  # optional cap per segment

def count_tokens(text: str) -> int:
    """Simple token count; can replace with more advanced tokenizer later"""
    return len(text.split())

def segment_blocks(blocks: list, max_tokens: int = 1000) -> list:
    """
    Build segments from a list of blocks.
    Each segment contains <= max_tokens or <= MAX_BLOCKS blocks.
    """
    segments = []
    current = {
        "segment_id": gen_id("seg"),
        "block_ids": [],
        "blocks": [],
        "length_estimate": 0,
    }
    sequence = 1

    for block in blocks:
        block_tokens = block.get("tokens", count_tokens(block.get("content", "")))

        # Start new segment if over limit
        if current["length_estimate"] + block_tokens > max_tokens or len(current["blocks"]) >= MAX_BLOCKS:
            current["sequence"] = sequence
            segments.append(current)
            sequence += 1
            current = {
                "segment_id": gen_id("seg"),
                "block_ids": [],
                "blocks": [],
                "length_estimate": 0,
            }

        current["blocks"].append(block)
        current["block_ids"].append(block["block_id"])
        current["length_estimate"] += block_tokens

    # Add last segment
    if current["blocks"]:
        current["sequence"] = sequence
        segments.append(current)

    return segments
