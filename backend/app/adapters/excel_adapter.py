from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment
from io import BytesIO
from app.config.translations.i18n import get_translation, load_reverse_mapping
import base64
from app.config.settings import settings
from app.adapters.log_adapter import LogAdapter
from pathlib import Path
import os
from app.modules.common.helpers.chunk_list import chunk_list
from app.modules.common.helpers.translate_headers import translate_headers
from typing import Dict
from app.modules.common.helpers.extract_export_value import extract_export_value

class ExcelAdapter:
    
    def count_rows(self, file_path: str) -> int:
        with open(file_path, 'rb') as f:
            workbook = load_workbook(filename=f, read_only=True, data_only=True)
            sheet = workbook.active
            return sheet.max_row - 1
    
    def create_excel(self, data: list[dict], columns: list[str], relationships: Dict[str, str] = None, locale: str = settings.DEFAULT_LANGUAGE, sheet_name: str = 'Hoja 1') -> bytes:
        """
        Create a excel file from a list of dictionaries.
        args:
            data: list[dict] - Lista de diccionarios con los datos
            columns: list[str] - Lista de nombres de columnas
            locale: str - Código de idioma para las traducciones
            sheet_name: str - Nombre de la hoja
        return: bytes
        """
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = sheet_name
        
        for index, column_name in enumerate(columns, start=1):
            translated_value = get_translation(f"attributes.{column_name}", locale)
            cell = sheet.cell(row=1, column=index, value=translated_value.upper() if translated_value else column_name.upper())
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='top')

        for row_idx, row_data in enumerate(data, start=2):
            for col_idx, column_name in enumerate(columns, start=1):
                if relationships and column_name in relationships:
                    value = extract_export_value(row_data, column_name, relationships[column_name])
                else:
                    value = row_data.get(column_name, '')
                cell = sheet.cell(row=row_idx, column=col_idx, value=value)
                cell.alignment = Alignment(horizontal='left', vertical='top')
                
        excel_file = BytesIO()
        workbook.save(excel_file)
        excel_file.seek(0)
        return base64.b64encode(excel_file.getvalue()).decode('utf-8')
    
    
    def export_with_chunks(self, file_name: str, items: list, headers: list[str], retrieve_callback: callable, relationships: Dict[str, str] = None, locale: str = settings.DEFAULT_LANGUAGE, sheet_name: str = 'Hoja 1') -> Path:
        """
        Export any list of objects to Excel by chunks.
        args:
            file_name: base name of the file.
            items: list of IDs or base objects.
            chunk_size: size of the batch to process.
            headers: columns of the Excel.
            row_builder: function that receives an object and returns a dict with the data.
            fetcher: function that receives a list of items (e.g. IDs) and returns objects.
        Returns:
            Path to the Excel file.
        """
        if not os.path.isabs(file_name):
            file_name = os.path.abspath(file_name)
        
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = sheet_name
        
        translated_headers, header_mapping = translate_headers(headers, locale)
        
        excel_path = Path(file_name)
        directory = excel_path.parent
        
        directory.mkdir(parents=True, exist_ok=True)
        
        for col_idx, row_data in enumerate(translated_headers, start=1):
            cell = sheet.cell(row=1, column=col_idx)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.value = row_data.upper() if row_data else ''

        current_row = 2
        for chunk in chunk_list(items, settings.PROJECT_CHUNK_SIZE):
            objs = retrieve_callback(chunk)
            for obj in objs:
                for col_idx, column_name in enumerate(translated_headers, start=1):
                    if relationships and column_name in relationships:
                        value = extract_export_value(obj, column_name, relationships[column_name])
                    else:
                        value = obj.to_dict().get(column_name, '')
                    cell = sheet.cell(row=current_row, column=col_idx)
                    cell.alignment = Alignment(horizontal='left', vertical='top')
                    cell.value = value
                current_row += 1
        
        workbook.save(excel_path)
                    
        return excel_path
            
            
    def export_by_date_range(self, file_name: str, headers: list[str], retrieve_callback: callable, relationships: Dict[str, str] = None, locale: str = settings.DEFAULT_LANGUAGE, sheet_name: str = 'Hoja 1') -> Path:
        """
        Export data to Excel using a date range, continuing while there are results.
        args:
            file_name: base name of the file.
            headers: columns of the Excel.
            relationships: dictionary with the key of the relation and the key of the attribute to extract the value from the relation.
            retrieve_callback: function that receives an offset and returns objects or None if there are no more results.
            locale: language for translations.
        Returns:
            Path to the Excel file.
        """
        if not os.path.isabs(file_name):
            file_name = os.path.abspath(file_name)
            
        excel_path = Path(file_name)
        directory = excel_path.parent
        
        directory.mkdir(parents=True, exist_ok=True)
        
        translated_headers, header_mapping = translate_headers(headers, locale)
        
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = sheet_name
        
        for col_idx, row_data in enumerate(translated_headers, start=1):
            cell = sheet.cell(row=1, column=col_idx)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.value = row_data.upper() if row_data else ''
            
        offset = 1
        current_row = 2  # Mantener contador global de filas
        while objs := retrieve_callback(offset):
            for obj in objs:
                translated_row = {header_mapping[k]: v for k, v in obj.to_dict().items() if k in header_mapping}
                for col_idx, column_name in enumerate(translated_headers, start=1):
                    if relationships and column_name in relationships:
                        value = extract_export_value(obj, column_name, relationships[column_name])
                    else:
                        value = translated_row.get(column_name, '') 
                    cell = sheet.cell(row=current_row, column=col_idx)
                    cell.alignment = Alignment(horizontal='left', vertical='top')
                    cell.value = value
                current_row += 1  # Incrementar el contador global
            offset += 1
            
        workbook.save(excel_path)
        return excel_path
            
            
            
            
            
    def read_excel_with_chunks(self, file_path: str, chunk_size: int = settings.PROJECT_CHUNK_SIZE, locale: str = settings.DEFAULT_LANGUAGE, sheet_name: str = None):
        """
        Read Excel file with chunks, converting translated headers back to original field names.
        Args:
            file_path: Path to the Excel file (.xlsx)
            chunk_size: Size of each chunk
            locale: Language of the Excel headers (for reverse translation)
            sheet_name: Name of the sheet to read (if None, reads the active sheet)
        """
        try:
            file = open(file_path, 'rb')
            workbook = load_workbook(filename=file, read_only=True, data_only=True)
            if sheet_name:
                if sheet_name in workbook.sheetnames:
                    sheet = workbook[sheet_name]
                else:
                    sheet = workbook.active
            else:
                sheet = workbook.active

            reverse_mapping = load_reverse_mapping(locale)
            
            headers = []
            original_headers = []
            
            for cell in sheet[1]:
                header_value = cell.value.lower().replace(" ", "_") if cell.value else ""
                headers.append(header_value)
                
                if header_value.startswith("attributes."):
                    original_key = header_value.replace("attributes.", "")
                elif header_value in reverse_mapping:
                    original_key = reverse_mapping[header_value]
                else:
                    original_key = header_value
                
                original_headers.append(original_key)
            
            chunk = []
            row_count = 0
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not any(row):
                    continue
                    
                original_row = {}
                for i, value in enumerate(row):
                    if i < len(original_headers):
                        original_row[original_headers[i]] = value
                
                chunk.append(original_row)
                row_count += 1
                
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            
            if chunk:
                yield chunk
            
        except Exception as e:
            LogAdapter().error(f"Error reading Excel file: {e}")
        finally:
            file.close()
            if 'workbook' in locals():
                workbook.close()