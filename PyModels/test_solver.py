import unittest
from solver import solver, ode, ObjectBase

# import matplotlib.pyplot as plt


class Connection:
    def __init__(self) -> None:
        self.P1 = None
        self.P2 = None
        self.f1 = None
        self.f2 = None


class Node(ObjectBase):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name
        self.add_ode("P1", "dP1dt")
        self.add_ode("P2", "dP1dt")
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
        # plt.plot(t, y[0], "+-", label=names[0])
        # plt.plot(t, y[1], "+-", label=names[1])
        # plt.plot(t, y[2], "+-", label=names[2])
        # plt.plot(t, y[3], "+-", label=names[3])
        # plt.grid()
        # plt.legend()
        # plt.show()
        self.assertAlmostEqual(y[0][-1], 3.0049575048289983)
        self.assertAlmostEqual(y[1][-1], 4.004957504828998)
        self.assertAlmostEqual(y[2][-1], 2.9950424951710004)
        self.assertAlmostEqual(y[3][-1], 3.995042495171)


if __name__ == "__main__":
    unittest.main()
