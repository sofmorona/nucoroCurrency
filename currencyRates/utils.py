import datetime
import decimal
from functools import reduce

def checkDateFormat(date_string, format):
    """
    Function to check if the given date has the expected format
    :param date_string: string to check if is a valid date format
    :param format: the format expected by the date_string
    :return: datetime with the date of the string given, False if the string couldn't be converted.
    """
    try:
        return datetime.datetime.strptime(date_string, format)

    except ValueError:
        return False


def checkDecimal(value):
    """
    Function to check if the given value can be converted to decimal
    :param value: a value compatible with decimal conversion
    :return: the decimal in case it can be converted, false in other case
    """
    try:
        return decimal.Decimal(value)

    except decimal.InvalidOperation:
        return False

def calculate_twr(values):
    """​
    Function to calculate the time-weighted rate
    Formula:
        TWR=[(1+HP1)×(1+HP2)×...×(1+HPn)]−1
        where:
        TWR= Time-weighted return
        n=Number of sub-periods
        HP=(End Value − Initial Value + Cash Flow)/(Initial Value + Cash Flow)
        HPn = Return for sub-period n
    :param values: List of periods
    :param amount: amount for which we want to calculate the TWR
    :return: the TWR for the given amount
    """
    # @todo implement this function
    # What is exactly the cashFlow in the API request that we have
    # What are the sub-period?

    return {'twr': 0, 'rate_value': values[0].rate_value}

