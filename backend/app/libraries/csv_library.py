from io import StringIO, TextIOWrapper
import csv
from app.modules.common.helpers.encodeToBase64 import encode_to_base64
from app.modules.common.helpers.chunk_list import chunk_list
from pathlib import Path
from app.config.settings import settings
import os
from app.config.translations.i18n import load_reverse_mapping
from app.modules.common.helpers.translate_headers import translate_headers

class CsvLibrary:
    def __init__(self):
        pass
    
    def count_rows(self, file_path: str) -> int:
        with open(file_path, 'rb') as f:
            file_stream = TextIOWrapper(f, encoding='utf-8')
            total = sum(1 for _ in file_stream)
        return total
    
    def export_to_csv(self, data: list[dict], columns: list[str], locale: str):
        translated_columns, header_mapping = translate_headers(columns, locale)
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=translated_columns, extrasaction='ignore')
        writer.writeheader()
        
        for row in data:
            translated_row = {header_mapping[k]: v for k, v in row.items() if k in header_mapping}
            writer.writerow(translated_row)
            
        return encode_to_base64(output.getvalue())
    
    
    def export_with_chunks(self, file_name: str, items: list, headers: list[str], retrieve_callback: callable, locale: str = settings.DEFAULT_LANGUAGE) -> Path:
        """
        Export any list of objects to CSV by chunks.
        args:
            file_name: base name of the file.
            items: list of IDs or base objects.
            chunk_size: size of the batch to process.
            headers: columns of the CSV.
            row_builder: function that receives an object and returns a dict with the data.
            fetcher: function that receives a list of items (e.g. IDs) and returns objects.
        Returns:
            Path to the CSV file.
        """
        if not os.path.isabs(file_name):
            file_name = os.path.abspath(file_name)
            
        translated_headers, header_mapping = translate_headers(headers, locale)
        
        csv_path = Path(file_name)
        directory = csv_path.parent
        
        directory.mkdir(parents=True, exist_ok=True)

        with csv_path.open(mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=translated_headers, extrasaction='ignore')
            writer.writeheader()

            for chunk in chunk_list(items, settings.PROJECT_CHUNK_SIZE):
                objs = retrieve_callback(chunk)
                for obj in objs:
                    translated_row = {header_mapping[k]: v for k, v in obj.to_dict().items() if k in header_mapping}
                    writer.writerow(translated_row)

        return csv_path
    
    
    def export_by_date_range(self, file_name: str, headers: list[str], retrieve_callback: callable, locale: str = settings.DEFAULT_LANGUAGE) -> Path:
        """
        Export data to CSV using a date range, continuing while there are results.
        args:
            file_name: base name of the file.
            headers: columns of the CSV.
            retrieve_callback: function that receives an offset and returns objects or None if there are no more results.
            locale: language for translations.
        Returns:
            Path to the CSV file.
        """ 
        if not os.path.isabs(file_name):
            file_name = os.path.abspath(file_name)
            
        translated_headers, header_mapping = translate_headers(headers, locale)
        
        csv_path = Path(file_name)
        directory = csv_path.parent
        
        directory.mkdir(parents=True, exist_ok=True)

        with csv_path.open(mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=translated_headers, extrasaction='ignore')
            writer.writeheader()

            offset = 1
            while objs := retrieve_callback(offset):
                for obj in objs:
                    translated_row = {header_mapping[k]: v for k, v in obj.to_dict().items() if k in header_mapping}
                    writer.writerow(translated_row)
                offset += len(objs)

        return csv_path
    
            
    def read_csv_file_with_chunks(self, file_path: str, chunk_size: int = settings.PROJECT_CHUNK_SIZE, locale: str = settings.DEFAULT_LANGUAGE, delimiter: str = ','):
        """
        Read CSV file with chunks, converting translated headers back to original field names.
        Args:
            file_path: Path to the CSV file
            chunk_size: Size of each chunk
            locale: Language of the CSV headers (for reverse translation)
            delimiter: CSV delimiter to use (default: comma)
        """
        decoded_file = TextIOWrapper(open(file_path, 'rb'), encoding='utf-8')
        
        if delimiter == ',':
            sample = decoded_file.read(1024)
            decoded_file.seek(0)
            
            
            sniffer = csv.Sniffer()
            try:
                detected_delimiter = sniffer.sniff(sample, delimiters=";,|\t").delimiter
                if detected_delimiter != ',':
                    delimiter = detected_delimiter
            except csv.Error as e:
                comma_count = sample.count(',')
                semicolon_count = sample.count(';')
                pipe_count = sample.count('|')
                tab_count = sample.count('\t')
                
                delimiter_counts = {',': comma_count, ';': semicolon_count, '|': pipe_count, '\t': tab_count}
                most_common_delimiter = max(delimiter_counts, key=delimiter_counts.get)
                
                if delimiter_counts[most_common_delimiter] > 0:
                    delimiter = most_common_delimiter
        
        try:
            reader = csv.DictReader(decoded_file, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL, doublequote=True)
            first_row = next(reader)
            decoded_file.seek(0)
            
            if len(first_row) == 1 and delimiter in list(first_row.values())[0]:
                raise csv.Error("Malformed CSV detected")
            else:
                reader = csv.DictReader(decoded_file, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL, doublequote=True)
                
        except (csv.Error, StopIteration):
            decoded_file.seek(0)
            
            lines = decoded_file.readlines()
            repaired_lines = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                if i == 0:
                    repaired_lines.append(line)
                else:
                    if line.startswith('"') and not line.endswith('"'):
                        line = line[1:]
                    elif line.startswith('"') and line.endswith('"'):
                        line = line[1:-1]
                    
                    line = line.replace('""', '"')
                    
                    repaired_lines.append(line)
            
            repaired_content = '\n'.join(repaired_lines)
            
            from io import StringIO
            repaired_file = StringIO(repaired_content)
            reader = csv.DictReader(repaired_file, delimiter=delimiter)
        
        reverse_mapping = load_reverse_mapping(locale)
        
        chunk = []
        for row in reader:
            original_row = {}
            for translated_header, value in row.items():
                if translated_header.startswith("attributes."):
                    original_key = translated_header.replace("attributes.", "")
                elif translated_header in reverse_mapping:
                    original_key = reverse_mapping[translated_header]
                else:
                    original_key = translated_header
                
                original_row[original_key] = value
            
            chunk.append(original_row)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk