from app.adapters.log_adapter import LogAdapter

def extract_export_value(obj: any, field_key: str, relation_field: str) -> str:
    """
    Extract a value from an object and translate it if it's a dictionary
    Args:
        obj: The object to extract the value from
        field_key: The key to extract the value from
        relation_field: The key of the attribute to extract the value from the relation.
    Returns:
        The translated value
    """
    if isinstance(obj, dict):
        new_dict = obj.get(field_key, '')
        return new_dict.get(relation_field, '')
    else:
        attr = getattr(obj, field_key)
        return getattr(attr, relation_field)
    