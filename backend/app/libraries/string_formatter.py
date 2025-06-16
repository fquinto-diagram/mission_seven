
class StringFormatter:
    def sanitize(string: str) -> str:
        """
        Sanitizes a string by removing accents and special characters.
        Args:
            string (str): The string to sanitize.
            
        Returns:
            str: The sanitized string.
        """
        string = string.strip()
        
        replacements = {
            'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a', 'ª': 'a',
            'Á': 'A', 'À': 'A', 'Â': 'A', 'Ä': 'A',
            'é': 'e', 'è': 'e', 'ë': 'e', 'ê': 'e',
            'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
            'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i',
            'Í': 'I', 'Ì': 'I', 'Ï': 'I', 'Î': 'I',
            'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o',
            'Ó': 'O', 'Ò': 'O', 'Ö': 'O', 'Ô': 'O',
            'ú': 'u', 'ù': 'u', 'ü': 'u', 'û': 'u',
            'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
            'ñ': 'n', 'Ñ': 'N', 'ç': 'c', 'Ç': 'C'
        }
        
        for old, new in replacements.items():
            string = string.replace(old, new)
        
        special_chars = "\\¨º-~#@|!\"·$%&/()?'¡¿[^`]+}{¨´><;,.:€"
        for char in special_chars:
            string = string.replace(char, '')
            
        return string

    def remove_currency_symbol(string: str) -> str:
        """
        Removes the currency symbol from a string.
        Args:
            string (str): The string to remove the currency symbol from.
            
        Returns:
            str: The string without the currency symbol.
        """
        currency_symbols = ['€', '$', '£', '¥', '₽', '₩', '₹']
        for symbol in currency_symbols:
            string = string.replace(symbol, '')
        return string
