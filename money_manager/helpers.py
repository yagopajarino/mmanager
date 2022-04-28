


def ARS(value):
    """Format value as USD."""
    return f"$ {value:,.2f}"

def datetimeformat(value):
    format = "%m/%d/%Y"
    return value.strftime(format)