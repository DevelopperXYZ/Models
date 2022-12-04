import unittest
from derivative import derivative
from solver import solver
from th_properties import water0_properties
from thermohydraulic_monophasic import control_volume, pressure_loss


class test_thermohydraulic_monophasic(unittest.TestCase):
    def test_volume_pressure_loss(self):
        v1 = control_volume(name="v1", properties=water0_properties())
        v2 = control_volume(name="v2", properties=water0_properties())
        pl1 = pressure_loss(name="pl", cv_qm=1.0e-03)
        pl1.connect(v1, v2)

        v1._P = 2.0e5
        v1._T = 40.0
        v2._P = 1.0e5
        v2._T = 20.0

        s = solver()
        s._objects = [v1, v2, pl1]
        s.initialize()
        s.integrate(tspan=[0, 10.0], method="LSODA")

        self.assertAlmostEqual(v1._P, 1.5e5)
        self.assertAlmostEqual(v2._P, 1.5e5)


if __name__ == "__main__":
    unittest.main()
