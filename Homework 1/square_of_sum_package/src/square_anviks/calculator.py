from decimal import *


def square_of_sum(a, b):
    if type(a) not in (int, float, Decimal) or type(b) not in (int, float, Decimal):
        return -1
    return (a + b) ** 2
