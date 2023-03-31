import calendar
import datetime
import socket

from bottle import route, post, run, request, response

HEADER = """<html>
        <title>Расчёт погашения задолжности</title>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" 
                            integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" 
                            crossorigin="anonymous">
        </head>
        <div class="container">
        <div class="row justify-content-md-center">"""

FOOTER = """</div></div></html>"""

TABLE_HEAD = """
    <table class="table table-striped table-hover">
    <thead class="thead-inverse">
    <tr>
        <th>#</th><th>Дата</th><th>Остаток</th><th>Проценты</th>
    </tr>
    </thead><tbody>
    """

FORM = """
    <form action="/" method="post">
        <label for="summ">Остаток: </label>
        <input name="summ" type="text" class="form-control" id="summ" value="%s" autocomplete="off" required="True"/> 
        <br />

        <label for="percent">Процент:</label>
        <input name="percent" type="text" class="form-control" id="percent" value="%s" autocomplete="off" required="True"/> 
        <br />

        <label for="pay">Платёж:</label>
        <input name="pay" type="text" class="form-control" id="pay" autocomplete="off" required="True" /> <br />

        <label for="d_summ">Доп. сумма в конце:</label>
        <input name="d_summ" type="text" class="form-control" id="d_summ" autocomplete="off" /> <br />

        <input value="Расчитать" type="submit" class="btn btn-primary"/>
    </form>
    """

FOOTER_TABLE_PAGE = """</tbody> </table>
    <a href="/" class="underline-link small"> Назад </a>"""


def getlastdayinyear(year: int) -> int:
    t_d = datetime.datetime(year, 12, 31)
    return int(t_d.strftime("%j"))


def getlastdayinmonth(year: int, month: int) -> int:
    t_d = calendar.monthrange(year, month)
    return int(t_d[1])


def printdate(day: int, month: int, year: int) -> str:
    if month < 10:
        month = f"0{month}"
    return f"{day}.{month}.{year}"


def gettablerow(success: str, i: int, print_date: str, summ: float, percent_summ: float) -> str:
    return f"     <tr {success}><td>{i}</td><td>{print_date}</td><td>{summ}</td><td>{percent_summ}</td></tr>"


def calccalenadar(summ: float, d_summ: float, percent: float, pay: float) -> str:
    curr_date: datetime = datetime.datetime.now()
    year: int = curr_date.year
    month: int = curr_date.month - 1
    month: int = 12 if month < 1 else month
    days_year: int = getlastdayinyear(year)
    days_month: int = getlastdayinmonth(year, month)
    success: str = ""
    enabled_d_summ: bool = False

    # set cookies
    response.set_cookie("summ", str(summ))
    response.set_cookie("percent", str(percent))

    result = TABLE_HEAD

    i: int = 0
    while summ > 0:
        # сумма процента на текущий месяц
        percent_summ: float = round(
            (((summ / 100) * percent) / days_year) * days_month, 2
        )
        # если остаток+доп сумма уже меньше - вычтем
        if (summ <= pay + d_summ) and not enabled_d_summ:
            summ -= d_summ
            enabled_d_summ = True

        # остаток долг
        if summ >= pay:
            summ = round(summ - (pay - percent_summ), 2)
        else:
            summ = 0
            success = 'class="table-success"'
        month += 1
        i += 1

        if month > 12:
            month = 1
            year += 1
            days_year = getlastdayinyear(year)

        days_month = getlastdayinmonth(year, month)

        print_date = printdate(days_month, month, year)

        result += gettablerow(success, i, print_date, summ, percent_summ)

    return HEADER + result + FOOTER_TABLE_PAGE + FOOTER


@route("/")
def index():
    result: str = HEADER + FORM + FOOTER

    summ: str = request.get_cookie("summ") or ""
    percent: str = request.get_cookie("percent") or ""

    return result % (summ, percent)


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

    return calccalenadar(summ, d_summ, percent, pay)


if __name__ == "__main__":
    print(f"server ip: {socket.gethostbyname(socket.gethostname())}")
    run(host="0.0.0.0", port=8590, reloader=True)
