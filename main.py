from datetime import date, datetime
from typing import List

from bottle import post, request, route, run, static_file, template
from dateutil.parser import parse as du_parse
from dateutil.relativedelta import relativedelta

from consts import Consts
from func import (StrToIntDef, calc_calendar, calc_pay_to_date,
                  get_last_day_in_month)
from models import ClassResult


@route("/")
def index(err: str = None):
    # error: str = ""
    summ: str = request.get_cookie("summ") or ""
    percent: str = request.get_cookie("percent") or ""

    cur_year: int = datetime.now().year

    cur_month: int = datetime.now().month

    years_list: List = [*range(cur_year, cur_year + Consts.MORTGAGE_TERM)]

    return template(
        "index.tmpl",
        summ=summ,
        percent=percent,
        years_list=years_list,
        cur_month=cur_month,
        error=err,
        month_list=Consts.MONTH_DICT,
    )


@post("/")
def do_calc():
    summ: str = request.forms.get("summ") or "0"
    percent: str = request.forms.get("percent") or "0"
    pay: str = request.forms.get("pay") or "0"
    d_summ: str = request.forms.get("d_summ") or "0"

    summ: float = float(summ.replace(",", "."))
    percent: float = float(percent.replace(",", "."))
    pay: float = float(pay.replace(",", "."))
    d_summ: float = float(d_summ.replace(",", "."))

    table_row: ClassResult = calc_calendar(summ, d_summ, percent, pay)

    if table_row.isEmpty():
        return index(Consts.ERROR_MSG)

    return template("result.tmpl", result=table_row.get())


@route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="./static")


@post("/paytodate", method=["POST"])
def pay_to_date():
    summ: str = request.forms.get("summ_t_d") or "0"
    summ: float = float(summ.replace(",", "."))

    percent: str = request.forms.get("percent_t_d") or "0"
    percent: float = float(percent.replace(",", "."))

    month: str = request.forms.get("month") or "0"
    year: str = request.forms.get("year") or "0"

    month: int = StrToIntDef(month, 0)

    year: int = StrToIntDef(year, 0)

    # текущая дата
    curr_date: datetime = datetime.now()

    # проверим даты
    if month < 1 or month > 12:
        return index(Consts.ERROR_DATE)

    if year < curr_date.year or year > (curr_date.year + Consts.MORTGAGE_TERM):
        return index(Consts.ERROR_DATE)

    # Последний день в месяце
    day: int = get_last_day_in_month(year, month)

    tmp_finish_date: str = f"{day}.{month}.{year}"

    # тут нужна проверка на дату
    finish_date: date = du_parse(tmp_finish_date)
    delta: relativedelta = relativedelta(finish_date, curr_date)

    if finish_date <= curr_date:
        return index(Consts.ERROR_DELTA)

    pay_sum_to_date: float = calc_pay_to_date(summ, percent, delta)

    if pay_sum_to_date <= -1:
        return index(Consts.ERROR_CALC_TO_DATE)

    table_row: ClassResult = calc_calendar(summ, 0, percent, pay_sum_to_date)
    return template("result.tmpl", result=table_row.get())


if __name__ == "__main__":
    run(host="0.0.0.0", port=8590, reloader=True)
