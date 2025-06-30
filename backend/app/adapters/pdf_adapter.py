from weasyprint import HTML
from app.config.pdf import PDF_CONFIG
from app.config.jinja import create_jinja_environment


class PDFAdapter:
    def __init__(self):
        self.env = create_jinja_environment(PDF_CONFIG['TEMPLATES_DIR'])

    def download(self, template_name: str, context: dict) -> bytes:
        """
        Download a PDF from a template and context.
        Args:
            template_name (str): The name of the template to use.
            context (dict): The context to pass to the template.
        Returns:
            bytes: The PDF as bytes.
        """
        template = self.env.get_template(template_name)
        html = template.render(context)
        return HTML(string=html).write_pdf()
