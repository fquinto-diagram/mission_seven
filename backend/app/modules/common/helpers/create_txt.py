
def create_txt(file_path: str, data: list):
    """
    Create a txt file with the data
    Args:
        file_path (str): The path to the file
        data (list): The data to write to the file
    """
    with open(file_path, 'w') as file:
        for item in data:
            file.write(f"{item}\n")
            
            
def create_txt_from_dict(file_path: str, data: dict):
    """
    Create a txt file with the data
    Args:
        file_path (str): The path to the file
        data (dict): The data to write to the file
    """
    with open(file_path, 'w') as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")