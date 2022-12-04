from numpy import sqrt


def sqrt_modif(x: float, dx: float) -> float:
    """
    Square root function with non infinite derivtive on 0
    """
    if x > 0:
        return sqrt(x + dx) - sqrt(dx)
    else:
        return -sqrt(-x + dx) + sqrt(dx)
