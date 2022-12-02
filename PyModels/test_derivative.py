import unittest
from derivative import *
from math import pi


class test_derivative(unittest.TestCase):
    def test_assign(self):
        x1 = derivative(12.36, 1)
        x2 = x1
        x1 = "xxx"
        self.assertAlmostEqual(x2.val(), 12.36)
        self.assertAlmostEqual(x2.val(1), 1.0)

    def test_pos(self):
        x1 = derivative(1.0, 0)
        x2 = +x1
        x1 = derivative(2.0, 1)
        self.assertAlmostEqual(str(x2), "1.0 1.0<0>")

    def test_neg(self):
        x1 = derivative(1.0, 0)
        x2 = -x1
        x1 = derivative(2.0, 1)
        self.assertAlmostEqual(str(x2), "-1.0 -1.0<0>")

    def test_eq(self):
        x1 = derivative(1.0, 0)
        x2 = derivative(1.0, 1)
        self.assertTrue(x1 == x2)

    def test_neq(self):
        x1 = derivative(1.0, 0)
        x2 = derivative(2.0, 1)
        self.assertTrue(x1 != x2)

    def test_gt(self):
        x1 = derivative(1.0, 0)
        x2 = derivative(2.0, 1)
        self.assertTrue(x2 > x1)

    def test_lt(self):
        x1 = derivative(1.0, 0)
        x2 = derivative(2.0, 1)
        self.assertTrue(x1 < x2)

    def test_ge(self):
        x1 = derivative(-7.1, 0)
        x2 = derivative(-7.1, 1)
        self.assertTrue(x1 >= x2)

    def test_le(self):
        x1 = derivative(0.0, 0)
        x2 = derivative(0.0, 1)
        self.assertTrue(x1 <= x2)

    def test_add(self):
        x1 = derivative(-12.3, 0)
        x2 = derivative(7, 3)
        x3 = x1 + x2
        self.assertAlmostEqual(x3.val(), -5.3)
        self.assertAlmostEqual(x3.val(0), 1.0)
        self.assertAlmostEqual(x3.val(3), 1.0)
        x3 = x1
        x3 += x2
        x2 = x1 = 0
        self.assertAlmostEqual(x3.val(), -5.3)
        self.assertAlmostEqual(x3.val(0), 1.0)
        self.assertAlmostEqual(x3.val(3), 1.0)

    def test_subs(self):
        x1 = derivative(-12.3, 0)
        x2 = derivative(7, 3)
        x3 = x1 - x2
        self.assertAlmostEqual(x3.val(), -19.3)
        self.assertAlmostEqual(x3.val(0), 1.0)
        self.assertAlmostEqual(x3.val(3), -1.0)
        x3 = x1
        x3 -= x2
        self.assertAlmostEqual(x3.val(), -19.3)
        self.assertAlmostEqual(x3.val(0), 1.0)
        self.assertAlmostEqual(x3.val(3), -1.0)

    def test_mult(self):
        x1 = derivative(-12.3, 0)
        x2 = derivative(7, 3)
        x3 = x1 * x2
        self.assertAlmostEqual(x3.val(), -86.1)
        self.assertAlmostEqual(x3.val(0), 7.0)
        self.assertAlmostEqual(x3.val(3), -12.3)
        x3 = x1
        x3 *= x2
        self.assertAlmostEqual(x3.val(), -86.1)
        self.assertAlmostEqual(x3.val(0), 7.0)
        self.assertAlmostEqual(x3.val(3), -12.3)

    def test_div(self):
        x1 = derivative(52.3, 0)
        x2 = derivative(-70.5e5, 3)
        x3 = x1 / x2
        self.assertAlmostEqual(x3.val(), -7.418439716312057e-06)
        self.assertAlmostEqual(x3.val(0), -1.4184397163120568e-07)
        self.assertAlmostEqual(x3.val(3), -1.0522609526683768e-12)
        x3 = x1
        x3 /= x2
        self.assertAlmostEqual(x3.val(), -7.418439716312057e-06)
        self.assertAlmostEqual(x3.val(0), -1.4184397163120568e-07)
        self.assertAlmostEqual(x3.val(3), -1.0522609526683768e-12)

    def test_radd(self):
        x1 = derivative(-125.0, 5)
        x2 = int(6) + x1
        self.assertAlmostEqual(x2.val(), -119.0)
        self.assertAlmostEqual(x2.val(5), 1.0)
        x2 = float(6.1) + x1
        self.assertAlmostEqual(x2.val(), -118.9)
        self.assertAlmostEqual(x2.val(5), 1.0)

    def test_rsubs(self):
        x1 = derivative(-125.0, 5)
        x2 = int(6) - x1
        self.assertAlmostEqual(x2.val(), 131.0)
        self.assertAlmostEqual(x2.val(5), -1.0)
        x2 = float(6.1) - x1
        self.assertAlmostEqual(x2.val(), 131.1)
        self.assertAlmostEqual(x2.val(5), -1.0)

    def test_rmult(self):
        x1 = derivative(10, 5)
        x2 = int(6) * x1
        self.assertAlmostEqual(x2.val(), 60)
        self.assertAlmostEqual(x2.val(5), 6)
        x2 = float(6.1) * x1
        self.assertAlmostEqual(x2.val(), 61.0)
        self.assertAlmostEqual(x2.val(5), 6.1)

    def test_rdiv(self):
        x1 = derivative(-12, 5)
        x2 = int(6) / x1
        self.assertAlmostEqual(x2.val(), -0.5)
        self.assertAlmostEqual(x2.val(5), -0.041666666666666664)
        x2 = float(6.0) / x1
        self.assertAlmostEqual(x2.val(), -0.5)
        self.assertAlmostEqual(x2.val(5), -0.041666666666666664)

    def test_exp_log(self):
        x1 = derivative(1.0, 0)
        r = exp(log(x1))
        self.assertAlmostEqual(r.val(), 1.0)
        self.assertAlmostEqual(r.val(0), 1.0)

    def test_sqrt(self):
        x1 = derivative(4.0, 1)
        x2 = sqrt(x1)
        self.assertAlmostEqual(x2.val(), 2.0)
        self.assertAlmostEqual(x2.val(1), 0.25)

    def test_sin(self):
        x1 = derivative(pi / 4.0, 0)
        x2 = sin(x1)
        self.assertAlmostEqual(x2.val(), sqrt(2.0) / 2.0)
        self.assertAlmostEqual(x2.val(0), sqrt(2.0) / 2.0)
        x2 = arcsin(sin(x1))
        self.assertAlmostEqual(x1.val(), x2.val())
        self.assertAlmostEqual(x1.val(0), x2.val(0))

    def test_cos(self):
        x1 = derivative(pi / 3.0, 0)
        x2 = cos(x1)
        self.assertAlmostEqual(x2.val(), 0.5)
        self.assertAlmostEqual(x2.val(0), -sqrt(3.0) / 2.0)
        x2 = arccos(cos(x1))
        self.assertAlmostEqual(x1.val(), x2.val())
        self.assertAlmostEqual(x1.val(0), x2.val(0))

    def test_tan(self):
        x1 = derivative(pi / 4.0, 0)
        x2 = tan(x1)
        self.assertAlmostEqual(x2.val(), 1.0)
        self.assertAlmostEqual(x2.val(0), 2.0)
        x2 = arctan(tan(x1))
        self.assertAlmostEqual(x1.val(), x2.val())
        self.assertAlmostEqual(x1.val(0), x2.val(0))

    def test_sinh(self):
        x1 = derivative(20.12, 0)
        x2 = sinh(x1)
        self.assertAlmostEqual(x2.val(), sinh(x1.val()))
        self.assertAlmostEqual(x2.val(0), cosh(x1.val()))
        x2 = arcsinh(sinh(x1))
        self.assertAlmostEqual(x1.val(), x2.val())
        self.assertAlmostEqual(x1.val(0), x2.val(0))

    def test_cosh(self):
        x1 = derivative(5.69, 0)
        x2 = cosh(x1)
        self.assertAlmostEqual(x2.val(), cosh(x1.val()))
        self.assertAlmostEqual(x2.val(0), sinh(x1.val()))
        x2 = arccosh(cosh(x1))
        self.assertAlmostEqual(x1.val(), x2.val())
        self.assertAlmostEqual(x1.val(0), x2.val(0))


if __name__ == "__main__":
    unittest.main()
