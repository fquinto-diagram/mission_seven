import importlib
import pkgutil
import sys
from app.modules.common.models.base_model import BaseModel
import inspect



def load_models(package_name: str = "app.modules"):
    """Import all models from app.modules.*.models.*, except common."""
    package = importlib.import_module(package_name)

    for finder, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        # Ignore everything under app.modules.common
        if module_name.startswith("app.modules.common"):
            continue

        # Only enter modules inside subfolders `models`
        if ".models." not in module_name:
            continue

        try:
            module = importlib.import_module(module_name)

            # Check if it contains classes that inherit from BaseModel (and not BaseModel or mixins)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseModel) and obj is not BaseModel and not obj.__name__.endswith("Mixin"):
                    break  # valid, we leave it loaded
            else:
                # No contains useful models, we clean it
                sys.modules.pop(module_name, None)

        except Exception as e:
            print(f"⚠️ Error importing {module_name}: {e}")
    
    
