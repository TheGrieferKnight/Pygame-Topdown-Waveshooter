import math


def round_if_float(n):

    if isinstance(n, float):

        frac, int_part = math.modf(n)

        if frac == 0.0:

            return int(int_part)

   

    return n