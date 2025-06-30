import json
from pathlib import Path
from polib import POFile, POEntry
import os

def convert_json_to_po(json_file: Path, po_file: Path):
    """Convert a JSON file of translations to a .po file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    po = POFile()
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': '',
        'POT-Creation-Date': '',
        'PO-Revision-Date': '',
        'Last-Translator': '',
        'Language-Team': '',
        'Language': json_file.stem,
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=UTF-8',
        'Content-Transfer-Encoding': '8bit',
    }
    
    def add_translations(translations, prefix=''):
        for key, value in translations.items():
            if isinstance(value, dict):
                add_translations(value, f"{prefix}{key}.")
            else:
                msgid = f"{prefix}{key}"
                entry = POEntry(msgid=msgid, msgstr=value)
                po.append(entry)
    
    add_translations(translations)
    po.save(po_file)

def main():
    translations_dir = Path(__file__).parent
    locales_dir = translations_dir / "locales"
    locales_dir.mkdir(exist_ok=True)
    
    # Convert each JSON file
    for json_file in translations_dir.glob("*.json"):
        locale = json_file.stem
        locale_dir = locales_dir / locale / "LC_MESSAGES"
        locale_dir.mkdir(parents=True, exist_ok=True)
        
        po_file = locale_dir / "messages.po"
        convert_json_to_po(json_file, po_file)
        print(f"Converted {json_file} to {po_file}")
        
        # Compile .po to .mo
        mo_file = locale_dir / "messages.mo"
        os.system(f"msgfmt {po_file} -o {mo_file}")
        print(f"Compiled {po_file} to {mo_file}")

if __name__ == "__main__":
    main() 