from .ids import gen_id

MAX_BLOCKS = 10

def new_segment():
    return {
        "segment_id": gen_id("seg"),
        "block_ids": [],
        "blocks": [],
        "length_estimate": 0,
    }

def segment_blocks(
    blocks: list,
    max_tokens: int = 1000,
    max_blocks: int = 10,
) -> list:

    segments = []
    current = new_segment()
    sequence = 1

    for block in blocks:

        block_tokens = block["tokens"]
        if (
            current["length_estimate"] + block_tokens > max_tokens
            or len(current["blocks"]) >= max_blocks
        ):
            current["sequence"] = sequence
            segments.append(current)
            sequence += 1
            current = new_segment()

        current["blocks"].append(block)
        current["block_ids"].append(block["block_id"])
        current["length_estimate"] += block_tokens

    if current["blocks"]:
        current["sequence"] = sequence
        segments.append(current)

    return segments
