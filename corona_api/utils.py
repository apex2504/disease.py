def format_date(dt):
    return dt.strftime('%d %b %Y %H:%M')

def format_number(number):
    if isinstance(number, int):
        return '{:,d}'.format(number)
    return '{:3.2f}'.format(number)
