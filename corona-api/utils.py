from datetime import datetime

def format_date(dt):
    return dt.strftime('%d %b %Y %H:%M')

def format_number(number):
    return '{:,d}'.format(number)