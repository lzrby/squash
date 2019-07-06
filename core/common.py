from datetime import datetime


def date_is_correct(date):
    if not isinstance(date, str):
        return False
    date_items = date.split('-')
    if len(date_items) != 3:
        return False
    for date_item in date_items:
        if not date_item.isdigit():
            return False
    if list(map(len, date_items[1:3])) != [2, 2]:
        return False
    year = int(date_items[0])
    if year < 1000 or year > 2100:
        return False
    month = int(date_items[1])
    if month < 1 or month > 12:
        return False
    day = int(date_items[2])
    months31 = [1, 3, 5, 7, 8, 10, 12]
    months30 = [4, 6, 9, 11]
    if month in months31:
        return day > 0 and day < 32
    elif month in months30:
        return day > 0 and day < 31
    else:
        if year % 4 != 0:
            return day > 0 and day < 29
        elif year % 100 == 0 and year % 400 != 0:
            return day > 0 and day < 29
        else:
            return day > 0 and day < 30


def today():
    cur_date = datetime.now()
    cur_year = str(cur_date.year)
    cur_month = f'{cur_date.month}'.rjust(2, '0')
    cur_day = '0' * (cur_date.day < 10) + str(cur_date.day)
    return f'{cur_year}-{cur_month}-{cur_day}'
