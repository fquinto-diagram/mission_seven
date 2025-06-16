


def chunk_list(list: list, chunk_size: int) -> list:
    """
    Chunk a list into smaller lists of a given size
    
    Args:
        list (list): The list to chunk
        chunk_size (int): The size of the chunks
        
    Returns:
        list: A list of chunks
    """
    return [list[i:i + chunk_size] for i in range(0, len(list), chunk_size)]

