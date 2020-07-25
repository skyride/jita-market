from django.utils.crypto import get_random_string


def chunker(items, chunk_size):
    """
    Chunk a list of items into chunks of the maximum defined size.
    """
    assert chunk_size > 0

    buffer = []
    for i, item in enumerate(items):
        buffer.append(item)

        # Yield buffer once it fills
        if len(buffer) % chunk_size == 0:
            yield buffer
            buffer = []

    # Yield last buffer if it contains items
    if len(buffer) > 0:
        yield buffer
