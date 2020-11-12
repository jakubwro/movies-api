from urllib.parse import quote

def format_arg(key, value):
    if value is None:
        return ""
    if isinstance(value, list):
        return "&".join([format_arg(key, v) for v in value])
    return f"{key}={quote(str(value))}"

def format_qurery_string(**kwargs):
    query = "&".join([format_arg(k, kwargs[k]) for k in kwargs if kwargs[k]])
    return query
