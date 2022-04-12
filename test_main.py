import unittest
import main


class Test(unittest.TestCase):
    def test_getlastdayinyear(self):
        """
        get last day in year
        """
        last_day = main.getlastdayinyear(2003)
        self.assertEqual(last_day, 365)

        last_day = main.getlastdayinyear(2000)
        self.assertEqual(last_day, 366)

    def test_getlastdayinmonth(self):
        """
        get last day in month
        """
        last_day = main.getlastdayinmonth(2003, 2)
        self.assertEqual(last_day, 28)

        last_day = main.getlastdayinmonth(2000, 2)
        self.assertEqual(last_day, 29)

    def test_printdate(self):
        """
        print date
        """
        day = main.printdate(2, 2, 2007)
        self.assertEqual(day, "2.02.2007")

        day = main.printdate(10, 11, 2007)
        self.assertEqual(day, "10.11.2007")


if __name__ == "__main__":
    unittest.main()
