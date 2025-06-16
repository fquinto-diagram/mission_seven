from pathlib import Path
import os

BASE_DIR = Path(os.path.join('app', 'modules'))

PDF_CONFIG = {
    "TEMPLATES_DIR": os.path.join(BASE_DIR, "templates"),
}
