import calendar
from datetime import datetime

from dateutil.relativedelta import relativedelta

from models import ClassResult


def StrToIntDef(intstr: str, default: int) -> int:
    try:
        result: int = int(intstr)
    except ValueError:
        result = default

    return result


def get_last_day_in_year(year: int) -> int:
    t_d = datetime(year, 12, 31)
    return int(t_d.strftime("%j"))


def get_last_day_in_month(year: int, month: int) -> int:
    t_d = calendar.monthrange(year, month)
    return int(t_d[1])


def print_date(day: int, month: int, year: int) -> str:
    if month < 10:
        month = f"0{month}"
    return f"{day}.{month}.{year}"


def calc_calendar(summ: float, d_summ: float, percent: float, pay: float) -> ClassResult:
    curr_date: datetime = datetime.now()
    year: int = curr_date.year
    month: int = curr_date.month
    # month: int = 1 if month == 0 else month
    days_year: int = get_last_day_in_year(year)
    days_month: int = get_last_day_in_month(year, month)
    success: str = ""
    enabled_d_summ: bool = False

    # класс для строчки таблицы
    table_row = ClassResult()

    # посчитаем проценты
    test_percent_summ: float = round((((summ / 100) * percent) / days_year) * days_month, 2)

    # При ошибке суммы выходим с пустой таблицей
    if pay <= test_percent_summ:
        return table_row

    i: int = 1
    while summ > 0:
        # сумма процента на текущий месяц
        percent_summ: float = round((((summ / 100) * percent) / days_year) * days_month, 2)
        # если остаток+доп сумма уже меньше - вычтем
        if (summ <= pay + d_summ) and not enabled_d_summ:
            summ -= d_summ
            enabled_d_summ = True

        # остаток долг
        if summ >= pay:
            summ = round(summ - (pay - percent_summ), 2)
        else:
            pay = round(summ + percent_summ, 2)
            summ = 0
            success = 'class="table-success"'

        print_date_data = print_date(days_month, month, year)

        table_row.add(success, i, print_date_data, summ, percent_summ, pay)

        month += 1
        i += 1

        if month > 12:
            month = 1
            year += 1
            days_year = get_last_day_in_year(year)

        days_month = get_last_day_in_month(year, month)

    # return HEADER + result + FOOTER_TABLE_PAGE + BACK_LINK + FOOTER
    return table_row


def get_count_payment_month(payment_summ: float, pay: float, percent: float, cur_date: datetime) -> int:
    year: int = cur_date.year
    month: int = cur_date.month - 1

    # для января
    month = 12 if month == 0 else month

    days_year: int = get_last_day_in_year(year)
    days_month: int = get_last_day_in_month(year, month)

    pay_days: int = 0
    while payment_summ > 0:
        # сумма процента на текущий месяц
        percent_summ: float = round((((payment_summ / 100) * percent) / days_year) * days_month, 2)

        # остаток долг
        payment_summ = round(payment_summ - (pay - percent_summ), 2) if payment_summ >= pay else 0
        month += 1
        pay_days += 1

        if month > 12:
            month = 1
            year += 1
            days_year = get_last_day_in_year(year)

        days_month = get_last_day_in_month(year, month)

    return pay_days


def calc_pay_to_date(summ: float, percent: float, delta: relativedelta) -> float:
    curr_date: datetime = datetime.now()

    # количество месяцев + текущий
    count_month = delta.years * 12 + delta.months + 1

    summ_percent: float = round((((summ / 100) * percent) / 12) * count_month, 2)

    result_summ: float = summ + summ_percent

    # платёж с процентами без учёта сложных процентов
    payment_with_percent: float = round(result_summ / count_month, 2)

    # платёж за чистый долг
    payment_without_percent: float = round(summ / count_month, 2)

    # delta_summ: int = round(payment_with_percent - payment_without_percent)

    # от суммы без процентов до суммы разности
    pays_list = [
        *range(
            round(payment_without_percent),
            round(payment_with_percent),
            10,
        )
    ]

    left = 0
    right = len(pays_list) - 1

    # бинарный поиск добавим, для скорости обработки
    while left <= right:
        center = (left + right) // 2
        test_count = get_count_payment_month(summ, pays_list[center], percent, curr_date)
        if count_month == test_count:
            # вернём сумму
            return pays_list[center]
        if count_month < test_count:
            left = center + 1
        else:
            right = center - 1

    return -1
