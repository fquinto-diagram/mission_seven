from app.libraries.number_formatter import NumberFormatter
from app.libraries.string_formatter import StringFormatter
class CurrencyFormatter:
    
    def format(amount: float | int, currency: str = '€', decimal_places: int = 2, thousands_separator: str = ".", decimal_separator: str = ",") -> str:
        """
        Formats a number as a currency string.
        
        Args:
            amount: The number to format.
            currency: The currency symbol to use.
            decimal_places: The number of decimal places to use.
            thousands_separator: The thousands separator to use.
            decimal_separator: The decimal separator to use.
        Returns:
            The formatted currency string.
        """
        return f"{NumberFormatter.format(amount, decimal_places, thousands_separator, decimal_separator)} {currency}"
    
    def unformat(amount: str) -> float:
        amount = StringFormatter.remove_currency_symbol(amount)
        return NumberFormatter.unformat(amount)
