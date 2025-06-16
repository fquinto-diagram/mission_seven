from jinja2 import Environment, FileSystemLoader
import os
from app.config.translations.i18n import get_translation

def create_jinja_environment(template_dir: str) -> Environment:
    """
    Create a Jinja2 environment with the standard global configuration.
    
    Args:
        template_dir (str): Directory where the templates are located
        
    Returns:
        Environment: Jinja2 environment configured
    """
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=True
    )
    
    # Standard global configuration
    env.globals.update({
        'get_translation': get_translation,
        'project_name': os.getenv('PROJECT_NAME'),
        'project_url': os.getenv('PROJECT_URL'),
        'frontend_url': os.getenv('FRONTEND_URL')
    })
    
    return env 