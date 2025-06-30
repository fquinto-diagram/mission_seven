from app.config.translations.i18n import get_translation

def translate_headers(headers: list[str], locale: str) -> list[str]:
    """
    Translate headers and create a mapping between original and translated headers.
    Args:
        headers: List of header names
        locale: Language for translations
    Returns:
        tuple containing translated headers list and mapping dictionary
    """
    translated_headers = []
    header_mapping = {}
    
    for header in headers:
        translated = get_translation(f"attributes.{header}", locale=locale)
        translated_headers.append(translated)
        header_mapping[header] = translated
        
    return translated_headers, header_mapping