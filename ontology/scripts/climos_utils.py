def strip(s: str):
    if not s:
        return s
    return s.strip().strip(' \t\n\r\f\v\u200b\u200c\u200d\ufeff').strip()
