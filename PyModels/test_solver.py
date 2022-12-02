import unittest
from solver import solver, ode


class Connection:
    def __init__(self) -> None:
        self.P1 = None
        self.P2 = None
        self.f1 = None
        self.f2 = None


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ode1 = ode(self, "P1", "dP1dt")
        self.ode2 = ode(self, "P2", "dP2dt")
        self.equations = [self.ode1, self.ode2]
        self.P1 = 1.0
        self.P2 = 2.0
        self.dP1dt = 1.0
        self.dP2dt = 2.0
        self.connections = list()

    def potential(self) -> None:
        for c in self.connections:
            c.P1 = self.P1
            c.P2 = self.P2

    def balance(self) -> None:
        f1 = 0.0
        f2 = 0.0
        for c in self.connections:
            f1 += c.f1
            f2 += c.f2
        self.dP1dt = f1
        self.dP2dt = f2


class Arc:
    def __init__(self, name: str) -> None:
        self.name = name
        self.c1 = Connection()
        self.c2 = Connection()

    def flux(self) -> None:
        f1 = self.c1.P1 - self.c2.P1
        f2 = 2.0 * (self.c1.P2 - self.c2.P2)
        self.c1.f1 = -f1
        self.c1.f2 = -f2

        self.c2.f1 = f1
        self.c2.f2 = f2

    def connect_nodes(self, n1: Node, n2: Node):
        n1.connections.append(self.c1)
        n2.connections.append(self.c2)


class test_solver(unittest.TestCase):
    def test_1(self):
        n1 = Node("n1")
        n2 = Node("n2")
        a = Arc("a")
        a.connect_nodes(n1, n2)

        s = solver(object_function_names=["potential", "flux", "balance"])
        s._objects = [n1, n2, a]
        s.initialize()

        n1.P1 = 5.0
        n1.P2 = 6.0
        t, y, names = s.integrate(tspan=[0, 3], method="LSODA")
        self.assertAlmostEqual(y[0][-1], 3.004957201640015)
        self.assertAlmostEqual(y[1][-1], 4.00001235911829)
        self.assertAlmostEqual(y[2][-1], 2.995042798359984)
        self.assertAlmostEqual(y[3][-1], 3.999987640881714)


if __name__ == "__main__":
    unittest.main()
