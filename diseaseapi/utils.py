def format_date(dt):
    """
    Outputs the date in a nice format; 01 Jan 1920 00:00
    """
    return dt.strftime('%d %b %Y %H:%M')

def parse_date(dt):
    """
    Split the datetime into individual parts, useful for formatting date yourself
    """
    return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second #returns format YEAR, MONTH, DAY, HOUR, MINUTE, SECOND

def format_number(number):
    """
    Formats a number to a more readable format; 10000 -> 10,000
    """
    if isinstance(number, int):
        return '{:,d}'.format(number)
    if number is None:
        return 'Unknown'
    return '{:3.2f}'.format(number)
