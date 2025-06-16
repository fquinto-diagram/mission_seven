from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.config.translations.i18n import get_translation
from zoneinfo import ZoneInfo

class DateFormatter:
    
    def current_datetime()-> datetime:
        """
        Get the current datetime in the Europe/Madrid timezone
        Returns:
            datetime: The current datetime
        """
        return datetime.now(ZoneInfo("Europe/Madrid"))

    def format(date: datetime, format: str = "%d.%m.%Y", include_time: bool = False)-> str:
        """
        Format a datetime object to a string
        Args:
            date (datetime): The datetime object to format
            format (str): The format to use for the string
            include_time (bool): Whether to include the time in the formatted string
        Returns:
            str: The formatted string
        """
        if include_time and '%H' not in format:
            format += ' %H:%M:%S'
        
        return date.strftime(format) 
    
    def format_formatted_date(date: str, format: str = "%d.%m.%Y", include_time: bool = False)-> str:
        """
        Format a formatted date to a datetime object
        Args:
            date (str): The formatted date to format
            format (str): The format to use for the datetime object
            include_time (bool): Whether to include the time in the datetime object
        Returns:
            datetime: The datetime object
        """
        if include_time and '%H' not in format:
            format += ' %H:%M:%S'
        
        return datetime.strptime(date, format).date()
    
    def unformat(date: str, format: str = "%d.%m.%Y", include_time: bool = False)-> datetime:
        """
        Unformat a string to a datetime object
        Args:
            date (str): The string to unformat
            format (str): The format to use for the datetime object
            include_time (bool): Whether to include the time in the datetime object
        Returns:
            datetime: The datetime object
        """
        if include_time:
            return datetime.strptime(date, format)
        
        return datetime.strptime(date, format).date()
    
    def increment_date_by_days(date: datetime = datetime.now(), days: int = 30)-> datetime:
        """
        Increment a date by a specified number of days
        Args:
            date (datetime): The date to increment
            days (int): The number of days to increment
        Returns:
            datetime: The incremented date
        """
        return date + timedelta(days)
    
    def increment_date_by_period(date: datetime = datetime.now(), period: str = "days", num_periods: int = 30)-> datetime:
        """
        Increment a date by a specified number of periods
        Args:
            date (datetime): The date to increment
            period (str): The period to increment
            num_periods (int): The number of periods to increment
        Returns:
            datetime: The incremented date
        """
        if period == "days":
            return date + timedelta(days=num_periods)
        elif period == "weeks":
            return date + timedelta(weeks=num_periods)
        elif period == "months":
            return date + relativedelta(months=num_periods)
        elif period == "years":
            return date + relativedelta(years=num_periods)
        
    def decrement_date_by_period(date: datetime = datetime.now(), period: str = "days", num_periods: int = 30)-> datetime:
        """
        Decrement a date by a specified number of periods
        Args:
            date (datetime): The date to decrement
            period (str): The period to decrement
            num_periods (int): The number of periods to decrement
        Returns:
            datetime: The decremented date
        """
        if period == "days":
            return date - timedelta(days=num_periods)
        elif period == "weeks":
            return date - timedelta(weeks=num_periods)
        elif period == "months":
            return date - relativedelta(months=num_periods)
        elif period == "years":
            return date - relativedelta(years=num_periods)

    def get_month_short_name(date: datetime = datetime.now())-> str:
        """
        Get the short name of the month of a date
        Args:
            date (datetime): The date to get the month short name
        Returns:
            str: The short name of the month
        """
        return get_translation("date_formatter.months.short." + date.strftime("%b"))
    
    def get_month_name(date: datetime = datetime.now())-> str:
        """
        Get the name of the month of a date
        Args:
            date (datetime): The date to get the month name
        Returns:
            str: The name of the month
        """
        return get_translation("date_formatter.months." + date.strftime("%B"))
    
    def get_month_digit(date: datetime = datetime.now())-> str:
        """
        Get the digit of the month of a date
        Args:
            date (datetime): The date to get the month digit
        Returns:
            str: The digit of the month
        """
        return date.strftime("%m")
    
    def get_year_digit(date: datetime = datetime.now())-> str:
        """
        Get the digit year of a date
        Args:
            date (datetime): The date to get the digit year
        Returns:
            str: The digit year
        """
        return date.strftime("%y")