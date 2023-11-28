from django import template
from datetime import datetime

register = template.Library()


# Format a timestamp as a string
@register.filter(name='format_timestamp')
def format_timestamp(timestamp, fmt=None):
    # Set a default format if none is provided
    if fmt is None:
        fmt = "%Y-%m-%d %H:%M:%S"

    try:
        date_time = datetime.fromtimestamp(int(timestamp))
        return date_time.strftime(fmt)
    except ValueError:
        return None
