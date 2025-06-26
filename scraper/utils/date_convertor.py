import datetime
import re

import nepali_datetime


class DateConvertor:
    @staticmethod
    def date_convertor(date_org):
        nepali_to_english_digit = str.maketrans("०१२३४५६७८९", "0123456789")

        nepali_months = {
            "वैशाख": 1,
            "जेठ": 2,
            "असार": 3,
            "साउन": 4,
            "भदौ": 5,
            "असोज": 6,
            "कात्तिक": 7,
            "मंसिर": 8,
            "पुस": 9,
            "पुष": 9,
            "माघ": 10,
            "फागुन": 11,
            "चैत": 12,
        }
        english_months = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }

        date_org = date_org.translate(nepali_to_english_digit)

        match = re.search(r"(\d+)\s+([^\s]+)\s+(\d+)\s+गते", date_org)

        if match:
            try:
                year = int(match.group(1))
                month_nep = match.group(2)
                day = int(match.group(3))

                month = nepali_months.get(month_nep)
                if not month:
                    return None

                nepali_dt = nepali_datetime.date(year, month, day)
                return nepali_dt.to_datetime_date()
            except Exception as e:
                print("Nepali date error:", e)
                return None

        match = re.search(r"([A-Za-z]{3}) (\d{1,2}), (\d{4})", date_org)
        if match:
            try:
                month_eng = match.group(1)
                day = int(match.group(2))
                year = int(match.group(3))

                month = english_months.get(month_eng)
                if not month:
                    return None

                return datetime.date(year, month, day)
            except Exception as e:
                print("English date error:", e)
                return None

        return None
