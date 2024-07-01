def to_iso_date(date_string: str):
    day, month, year = date_string.split(' ')[0].split('/')
    if len(year) < 4:
        prefix = '19' if int(year) >= 90 else '20'
        return '-'.join([prefix + year, month, day])
    return '-'.join([year, month, day])
