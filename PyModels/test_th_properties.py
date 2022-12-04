import unittest
import th_properties


class test_th_properties(unittest.TestCase):
    def test_1(self):
        property = th_properties.water0_properties()
        property.set_pt(1e5, 20)
        rho = property.rho()
        h = property.h()
        self.assertAlmostEqual(rho, 998.206543497)
        self.assertAlmostEqual(h, 84006.053943)


if __name__ == "__main__":
    unittest.main()
