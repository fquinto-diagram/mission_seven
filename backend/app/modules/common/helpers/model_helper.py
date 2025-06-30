def update_model_attributes(model, update_data: dict) -> None:
    """
    Update the attributes of a model with the provided data.
    
    Args:
        model: The model to update
        update_data (dict): Dictionary with the attributes and values to update
    """
    for key, value in update_data.items():
        print(key, value)
        if hasattr(model, key):
            setattr(model, key, value) 