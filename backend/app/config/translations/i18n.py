import gettext
from pathlib import Path
from app.config.settings import get_settings
import polib
from app.adapters.log_adapter import LogAdapter

TRANSLATIONS_DIR = Path(__file__).parent.parent / "translations" / "locales"

settings = get_settings()
_translations = {}

def _load_translation(locale: str):
    """Load a specific translation"""
    if locale not in _translations:
        try:
            translation = gettext.translation(
                'messages',
                localedir=str(TRANSLATIONS_DIR),
                languages=[locale]
            )
            _translations[locale] = translation
        except FileNotFoundError as e:
            _translations[locale] = gettext.NullTranslations()
    return _translations[locale]

def load_mapping(locale: str = None):
    """Load translation mapping from PO file"""
    if locale is None:
        locale = settings.DEFAULT_LANGUAGE
    
    po_file_path = TRANSLATIONS_DIR / locale / "LC_MESSAGES" / "messages.po"
    
    if not po_file_path.exists():
        return {}
    
    po = polib.pofile(str(po_file_path))
    return {entry.msgid: entry.msgstr for entry in po}

def load_reverse_mapping(locale: str = None) -> dict[str, str]:
    """
    Load reverse translation mapping from PO file (msgstr to msgid).
    This is used to convert CSV headers back from translations to original field names.
    Args:
        locale: Language code for the translations
    Returns:
        Dictionary mapping translated text to original msgid
    """
    if locale is None:
        locale = settings.DEFAULT_LANGUAGE
        
    reverse_mapping = {}
    
    po_file_path = TRANSLATIONS_DIR / locale / "LC_MESSAGES" / "messages.po"
    
    if not po_file_path.exists():
        return reverse_mapping
    
    try:
        po = polib.pofile(str(po_file_path))
        
        for entry in po:
            if entry.msgid.startswith("attributes.") and entry.msgstr:
                original_key = entry.msgid.replace("attributes.", "")
                reverse_mapping[entry.msgstr] = original_key
                
    except Exception as e:
        LogAdapter(f"Error loading reverse translation mapping: {e}")
        
    return reverse_mapping

def get_translation(key: str, locale: str = None, **kwargs) -> str:
    """
    Get a translation by its key and locale.
    
    Args:
        key (str): Translation key (eg: "errors.unauthorized")
        locale (str): Language code (eg: "es", "en")
        **kwargs: Additional arguments to format the translation
        
    Returns:
        str: Translated text
    """
    if locale is None:
        locale = get_settings().DEFAULT_LANGUAGE
        
    try:
        translation = _load_translation(locale)
        msg = translation.gettext(key)
        if msg != key:
            result = msg.format(**kwargs) if kwargs else msg
            return result
            
        parts = key.split('.')
        if len(parts) > 1:
            msg = translation.gettext(parts[-1])
            
            if msg != parts[-1]:
                result = msg.format(**kwargs) if kwargs else msg
                return result
                
        return key
    except Exception as e:
        return key

def set_locale(locale: str) -> None:
    """
    Set the default language.
    
    Args:
        locale (str): Language code (eg: "es", "en")
    """
    settings = get_settings()
    if locale in settings.AVAILABLE_LANGUAGES:
        settings.DEFAULT_LANGUAGE = locale
