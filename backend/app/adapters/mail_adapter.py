from fastapi_mail import FastMail, MessageSchema
from app.config.email import email_conf
from typing import List, Dict, Any, BinaryIO, TypedDict, Union
from fastapi import BackgroundTasks
import mimetypes
from io import BytesIO
from app.config.translations.i18n import get_translation
from pydantic import EmailStr
import os
from app.adapters.log_adapter import LogAdapter
from app.config.jinja import create_jinja_environment

class AsyncBytesIO(BytesIO):
    def __init__(self, content: bytes, filename: str):
        super().__init__(content)
        self.filename = filename

    async def read(self):
        return super().read()
    
    async def close(self):
        super().close()

class EmailAttachment(TypedDict):
    file: Union[BinaryIO, BytesIO, str]
    filename: str
    mime_type: str = None

class MailAdapter:
    def __init__(self, locale: str = "es"):
        self.fm = FastMail(email_conf)
        self.locale = locale
        self._setup_jinja()
        
    def _setup_jinja(self):
        template_dir = os.path.join("app", "modules", "templates", "mails")
        self.jinja_env = create_jinja_environment(template_dir)
        self.jinja_env.globals['get_translation'] = get_translation
        self.jinja_env.globals['locale'] = self.locale
        self.jinja_env.globals['project_name'] = os.getenv('PROJECT_NAME')
        self.jinja_env.globals['project_url'] = os.getenv('PROJECT_URL')
        self.jinja_env.globals['frontend_url'] = os.getenv('FRONTEND_URL')
        
    def _prepare_attachment(self, file: Union[BinaryIO, BytesIO, str, bytes], filename: str, mime_type: str = None) -> tuple:
        """
        Prepare an attachment for the email.
        
        Args:
            file: Can be a binary file, BytesIO, bytes or a file path
            filename: File name
            mime_type: File MIME type (optional)
            
        Returns:
            Tuple with (file_content, filename)
            
        Raises:
            ValueError: If the file type is not supported or the file doesn't exist
        """
        try:
            if isinstance(file, str):
                file_path = os.path.abspath(file)
                if not os.path.exists(file_path):
                    raise ValueError(get_translation("errors.file_not_found", file=file_path))
                with open(file_path, 'rb') as f:
                    file_content = f.read()
            elif isinstance(file, (BinaryIO, BytesIO)):
                file_content = file.read()
            elif isinstance(file, bytes):
                file_content = file
            else:
                raise ValueError(get_translation("errors.unsupported_file_type"))

            if not mime_type:
                mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            
            file_obj = AsyncBytesIO(file_content, filename)
            
            return (file_obj, filename)
        except Exception as e:
            LogAdapter.error(f"Error processing file: {e}")
            if isinstance(e, ValueError):
                raise e
            raise ValueError(get_translation("errors.file_processing_error", error=str(e)))

    def _prepare_message(self, template: str, to: Union[EmailStr, List[EmailStr]], body: Dict[str, Any] = {}, subject: str = "", bcc: List[EmailStr] = [], files: List[EmailAttachment] = []) -> MessageSchema:
        """
        Prepare an email message with template, recipients, body, subject and attachments.
        
        Args:
            template: Template name
            to: Recipients (EmailStr or list of EmailStr)
            body: Email body
            subject: Email subject
            bcc: List of hidden recipients
            files: List of attachments
            
        Returns:
            MessageSchema: Prepared message to send
        """
        recipients = [to] if isinstance(to, (str, EmailStr)) else to
        bcc = [bcc] if isinstance(bcc, (str, EmailStr)) else bcc
        template_obj = self.jinja_env.get_template(template)
        html_content = template_obj.render(**body)
        
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            bcc=bcc,
            body=html_content,
            subtype="html"
        )
        
        if files:
            for file_info in files:
                attachment = self._prepare_attachment(
                    file=file_info["file"],
                    filename=file_info["filename"],
                    mime_type=file_info.get("mime_type")
                )
                message.attachments.append(attachment)
                
        return message

    async def send_email(self, template: str, to: Union[EmailStr, List[EmailStr]], body: Dict[str, Any] = {}, subject: str = "", bcc: List[EmailStr] = [], files: List[EmailAttachment] = []) -> bool:
        """
        Send an email with a template, to, body, subject and files.
        
        Args:
            template: Template name
            to: Recipients (EmailStr or list of EmailStr)
            body: Body of the email
            subject: Subject of the email
            files: List of files to be attached to the email
            
        Returns:
            True if the email was sent successfully, False otherwise
            
        Examples:
            # Send email without attachments
            await mail.send_email(
                template="email.html",
                to="test@test.com",
                body={"name": "John Doe"},
                subject="Test Email"
            )
            
            # Send email to multiple recipients
            await mail.send_email(
                template="email.html",
                to=["test1@test.com", "test2@test.com"],
                body={"name": "John Doe"},
                subject="Test Email"
            )
            
            # Send email with attachment from a server path
            await mail.send_email(
                template="email.html",
                to="test@test.com",
                body={"name": "John Doe"},
                subject="Test Email",
                files=[{
                    "file": "path/to/file.pdf",
                    "filename": "file.pdf",
                    "mime_type": "application/pdf"  # opcional
                }]
            )
            
            # Send email with PDF generated with pdf adapter
            pdf_adapter = PDFAdapter()
            pdf_bytes = pdf_adapter.download(os.path.join("mails", "auth", "reset-password.html"), {
                "token": token,
                "name": user.name,
            })
            await mail.send_email(
                template="email.html",
                to="test@test.com",
                body={"name": "John Doe"},
                subject="Test Email",
                files=[{
                    "file": pdf_bytes,
                    "filename": "document.pdf",
                    "mime_type": "application/pdf"  # opcional
                }]
            )
            
            # Send email with file uploaded through a FastAPI endpoint
            content = await file.read()
            await mail.send_email(
                template="template.html",
                to="usuario@ejemplo.com",
                body={"name": "Usuario"},
                subject="Email with attachment",
                files=[{
                    "file": BytesIO(content),
                    "filename": file.filename,
                    "mime_type": file.content_type  # opcional
                }]
            )
        """
        try:
            message = self._prepare_message(template, to, body, subject, bcc, files)
            await self.fm.send_message(message)
            return True
        except Exception as e:
            LogAdapter.error(f"Error sending email: {e}")
            return False

    async def send_email_in_background(self, background_tasks: BackgroundTasks, template: str, to: Union[EmailStr, List[EmailStr]], body: Dict[str, Any] = {}, subject: str = "", bcc: List[EmailStr] = [], files: List[EmailAttachment] = []) -> bool:
        """
        Send an email in background with a template, to, body, subject and files.
        
        Args:
            background_tasks: BackgroundTasks object
            template: Template name
            to: Recipients (EmailStr or list of EmailStr)
            body: Body of the email
            subject: Subject of the email
            files: List of files to be attached to the email
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        try:
            message = self._prepare_message(template, to, body, subject, bcc, files)
            background_tasks.add_task(self.fm.send_message, message)
            return True
        except Exception as e:
            LogAdapter.error(f"Error sending email in background: {e}")
            return False
