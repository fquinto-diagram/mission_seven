import os
import tempfile
import puremagic
from fastapi import UploadFile
import shutil
from app.modules.common.helpers.storage_path import storage_path
from datetime import datetime
from app.adapters.log_adapter import LogAdapter
import zipfile
from io import BytesIO
import mimetypes

class FileLibrary:
    
    CHUNK_SIZE: int = 1024 * 1024
    
    MAGIC_PATTERNS = {
        # Certificados Digitales
        'application/x-pkcs12': [
            b'\x30\x82',  # PKCS#12 (P12/PFX) - ASN.1 DER
        ],
        'application/x-x509-ca-cert': [
            b'\x30\x82',  # X.509 certificates (DER)
        ],
        
        # PDFs
        'application/pdf': [
            b'%PDF-',  # PDF signature
        ],
        
        # Imágenes mejoradas
        'image/jpeg': [
            b'\xFF\xD8\xFF\xE0',  # JPEG JFIF
            b'\xFF\xD8\xFF\xE1',  # JPEG EXIF
            b'\xFF\xD8\xFF\xE2',  # JPEG (Canon)
            b'\xFF\xD8\xFF\xE3',  # JPEG (Samsung)
            b'\xFF\xD8\xFF\xE8',  # JPEG SPIFF
            b'\xFF\xD8\xFF\xDB',  # JPEG without metadata
            b'\xFF\xD8\xFF\xEE',  # JPEG
        ],
        'image/png': [
            b'\x89PNG\r\n\x1a\n',  # PNG signature
        ],
        'image/gif': [
            b'GIF87a',  # GIF87a
            b'GIF89a',  # GIF89a
        ],
        'image/webp': [
            b'RIFF',  # WebP (needs additional check)
        ],
        'image/bmp': [
            b'BM',  # BMP signature
        ],
        'image/tiff': [
            b'II*\x00',  # TIFF little endian
            b'MM\x00*',  # TIFF big endian
        ],
        'image/x-icon': [
            b'\x00\x00\x01\x00',  # ICO format
            b'\x00\x00\x02\x00',  # CUR format
        ],
        
        # Archivos comprimidos (RAR solamente, ZIP se maneja por separado)
        'application/x-rar-compressed': [
            b'Rar!\x1a\x07\x00',  # RAR v4
            b'Rar!\x1a\x07\x01\x00',  # RAR v5
        ],
    }
    
    @staticmethod
    async def get_mime_type(file: UploadFile) -> str | None:
        try:
            # Leer contenido del archivo
            await file.seek(0)
            full_content = await file.read()
            await file.seek(0)
            
            if not full_content:
                return None
            
            # Verificar primero si es un archivo ZIP-based (OpenXML o ZIP genérico)
            if full_content.startswith(b'PK\x03\x04') or full_content.startswith(b'PK\x05\x06') or full_content.startswith(b'PK\x07\x08'):
                openxml_type = FileLibrary._detect_openxml_type(full_content)
                if openxml_type != 'application/zip':
                    return openxml_type
                else:
                    return 'application/zip'
            
            custom_mime = FileLibrary._detect_with_magic_patterns(full_content)
            if custom_mime:
                return custom_mime
                
            header = full_content[:4096] if len(full_content) >= 4096 else full_content
            mime_type = puremagic.from_string(header, mime=True)
            
            if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return FileLibrary._detect_openxml_type(full_content)
            
            if mime_type in ['application/octet-stream', None] and FileLibrary._is_certificate(full_content):
                return FileLibrary._detect_certificate_type(full_content)
            
            if not mime_type and file.filename:
                mime_type, _ = mimetypes.guess_type(file.filename)
            
            return mime_type
            
        except Exception as e:
            LogAdapter.error(f"Error getting mime type: {str(e)}")
            try:
                await file.seek(0)
            except:
                pass
            return None
    
    @staticmethod
    def _detect_with_magic_patterns(content: bytes) -> str | None:
        """Detect mime types using custom magic bytes patterns"""
        for mime_type, patterns in FileLibrary.MAGIC_PATTERNS.items():
            for pattern in patterns:
                if content.startswith(pattern):
                    if mime_type == 'image/webp' and len(content) > 12:
                        if content[8:12] == b'WEBP':
                            return mime_type
                        continue
                    return mime_type
        return None
    
    @staticmethod
    def _detect_openxml_type(content: bytes) -> str:
        """Detect specific OpenXML file type (Excel, Word, PowerPoint) or generic ZIP"""
        try:
            with zipfile.ZipFile(BytesIO(content)) as zip_file:
                if '[Content_Types].xml' in zip_file.namelist():
                    content_types = zip_file.read('[Content_Types].xml').decode('utf-8')
                    
                    if 'spreadsheetml.sheet' in content_types:
                        return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    elif 'wordprocessingml.document' in content_types:
                        return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                    elif 'presentationml.presentation' in content_types:
                        return 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
                
                return 'application/zip'
        except (zipfile.BadZipFile, UnicodeDecodeError):
            return 'application/zip'
    
    @staticmethod
    def _is_certificate(content: bytes) -> bool:
        """Check if the content could be a digital certificate"""
        certificate_patterns = [
            b'-----BEGIN CERTIFICATE-----',
            b'-----BEGIN PRIVATE KEY-----',
            b'-----BEGIN RSA PRIVATE KEY-----',
            b'-----BEGIN PKCS7-----',
            b'\x30\x82',  # ASN.1 DER encoding
        ]
        
        for pattern in certificate_patterns:
            if pattern in content[:1024]:
                return True
        return False
    
    @staticmethod
    def _detect_certificate_type(content: bytes) -> str:
        """Detect specific certificate type"""
        if b'-----BEGIN' in content[:100]:
            if b'CERTIFICATE' in content[:200]:
                return 'application/x-pem-file'
            elif b'PRIVATE KEY' in content[:200]:
                return 'application/x-pem-file'
            elif b'PKCS7' in content[:200]:
                return 'application/pkcs7-mime'
        
        # DER/Binary certificates
        if content.startswith(b'\x30\x82'):
            if len(content) > 20:
                if b'\x30\x80' in content[:50] or b'\x04\x14' in content[:50]:
                    return 'application/x-pkcs12'
                else:
                    return 'application/x-x509-ca-cert'
        
        return 'application/x-x509-ca-cert'
    
    @staticmethod
    async def get_file_size(file: UploadFile) -> int:
        total = 0
        while True:
            chunk = await file.read(FileLibrary.CHUNK_SIZE)
            if not chunk:
                break
            total += len(chunk)
        await file.seek(0)
        return total
    
    @staticmethod
    async def temp_file(file: UploadFile, user_id: int = None) -> str:
        if user_id:
            storage_dir = storage_path("companies", str(user_id), "tmp")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            file_path = storage_dir / filename
        else:
            tmp = tempfile.NamedTemporaryFile(delete=False)
            file_path = tmp.name
            
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        await file.seek(0) 
        return str(file_path)
    
    @staticmethod
    def delete_file(file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            LogAdapter.error(f"Error deleting file {file_path}: {str(e)}")