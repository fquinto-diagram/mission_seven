from pathlib import Path
import os

def storage_path(*directories: str) -> Path:
    """
    Return the path to the storage directory with the specified subdirectories.
    
    Args:
        *directories: List of subdirectories to access
        
    Returns:
        Path: Full path to the storage directory
    """
    base_dir = Path('/app').absolute()
    storage_path = base_dir / "storage"
    
    storage_path.mkdir(parents=True, exist_ok=True)
    
    if directories:
        storage_path = storage_path.joinpath(*directories)
        storage_path.mkdir(parents=True, exist_ok=True)
        
    return Path(os.path.abspath(str(storage_path)))
