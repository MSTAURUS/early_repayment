import unittest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from func import StrToIntDef, get_last_day_in_year, get_last_day_in_month, print_date, calc_calendar, \
    get_count_payment_month, calc_pay_to_date


class TestFunctions(unittest.TestCase):
    def test_StrToIntDef_ValidInt(self):
        # Arrange
        intstr = "42"
        default = 0
        expected = 42

        # Act
        result = StrToIntDef(intstr, default)

        # Assert
        self.assertEqual(result, expected)

    def test_StrToIntDef_InvalidInt(self):
        # Arrange
        intstr = "notanint"
        default = 0
        expected = 0

        # Act
        result = StrToIntDef(intstr, default)

        # Assert
        self.assertEqual(result, expected)

    def test_StrToIntDef_EmptyString(self):
        # Arrange
        intstr = ""
        default = 10
        expected = 10

        # Act
        result = StrToIntDef(intstr, default)

        # Assert
        self.assertEqual(result, expected)

    def test_get_last_day_in_year_LeapYear(self):
        # Arrange
        year = 2020
        expected = 366

        # Act
        result = get_last_day_in_year(year)

        # Assert
        self.assertEqual(result, expected)

    def test_get_last_day_in_year_CommonYear(self):
        # Arrange
        year = 2021
        expected = 365

        # Act
        result = get_last_day_in_year(year)

        # Assert
        self.assertEqual(result, expected)

    def test_get_last_day_in_month_CommonYear_Feb(self):
        # Arrange
        year = 2021
        month = 2
        expected = 28

        # Act
        result = get_last_day_in_month(year, month)

        # Assert
        self.assertEqual(result, expected)

    def test_get_last_day_in_month_LeapYear_Feb(self):
        # Arrange
        year = 2020
        month = 2
        expected = 29

        # Act
        result = get_last_day_in_month(year, month)

        # Assert
        self.assertEqual(result, expected)

    def test_get_last_day_in_month_April(self):
        # Arrange
        year = 2021
        month = 4
        expected = 30

        # Act
        result = get_last_day_in_month(year, month)

        # Assert
        self.assertEqual(result, expected)

    def test_get_last_day_in_month_December(self):
        # Arrange
        year = 2021
        month = 12
        expected = 31

        # Act
        result = get_last_day_in_month(year, month)

        # Assert
        self.assertEqual(result, expected)

    def test_print_date_JanFirst(self):
        # Arrange
        day = 1
        month = 1
        year = 2021
        expected = "1.01.2021"

        # Act
        result = print_date(day, month, year)

        # Assert
        self.assertEqual(result, expected)

    def test_print_date_DecLast(self):
        # Arrange
        day = 31
        month = 12
        year = 2021
        expected = "31.12.2021"

        # Act
        result = print_date(day, month, year)

        # Assert
        self.assertEqual(result, expected)

    def test_print_date_MidYear(self):
        # Arrange
        day = 15
        month = 5
        year = 2021
        expected = "15.05.2021"

        # Act
        result = print_date(day, month, year)

        # Assert
        self.assertEqual(result, expected)

    def test_calc_calendar_SimpleCase(self):
        # Arrange
        summ = 1000.0
        d_summ = 100.0
        percent = 10.0
        pay = 200.0
        expected = "Expected ClassResult Object"

        # Act
        result = calc_calendar(summ, d_summ, percent, pay)

        # Assert Length
        self.assertEqual(result.len(), 5)
        self.assertEqual(result.get()[0]["summ"], 808.47)
        self.assertEqual(result.get()[1]["summ"], 614.88)
        self.assertEqual(result.get()[2]["summ"], 420.09)
        self.assertEqual(result.get()[3]["summ"], 223.53)
        self.assertEqual(result.get()[4]["summ"], 0)

        # Assert success
        self.assertIsNotNone(result.get()[4]["success"])

    def test_get_count_payment_month_SimpleCase(self):
        # Arrange
        payment_summ = 1000.0
        pay = 200.0
        percent = 10.0
        cur_date = datetime(2021, 1, 1)
        expected = 6

        # Act
        result = get_count_payment_month(payment_summ, pay, percent, cur_date)

        # Assert
        self.assertEqual(result, expected)

    def test_calc_pay_to_date_SimpleCase(self):
        # Arrange
        summ = 5286594.96
        percent = 6.4
        delta = relativedelta(years=1)
        expected = 427801

        # Act
        result = calc_pay_to_date(summ, percent, delta)

        # Assert
        self.assertEqual(result, expected)

        # Arrange
        summ = 5286594.96
        percent = 6.4
        delta = relativedelta(month=1)
        expected = 5300685

        # Act
        result = calc_pay_to_date(summ, percent, delta)

        # Assert
        self.assertEqual(result, expected)

        # Arrange
        summ = 5286594.96
        percent = 6.4
        delta = relativedelta(years=9, months=2)
        expected = 63477

        # Act
        result = calc_pay_to_date(summ, percent, delta)

        # Assert
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
