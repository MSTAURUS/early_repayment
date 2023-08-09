import datetime
from typing import Dict, List


class ClassResult:
    def __init__(self):
        self.__data = []

    def add(
        self,
        success: str,
        num: int,
        print_date: datetime,
        summ: float,
        percent_summ: float,
        pay: float,
    ) -> None:
        table_row: Dict = dict.fromkeys(["success", "num", "print_date", "summ", "percent_summ"])
        table_row["success"] = success
        table_row["num"] = num
        table_row["pay"] = pay
        table_row["print_date"] = print_date
        table_row["summ"] = summ
        table_row["percent_summ"] = percent_summ
        self.__data.append(table_row.copy())

    def get(self) -> List:
        return self.__data

    def isEmpty(self):
        return len(self.__data) == 0
