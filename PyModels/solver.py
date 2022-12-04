import matplotlib.pyplot as plt
from derivative import derivative
from scipy.integrate import solve_ivp


class ode:
    def __init__(self, object_adress, x_name: str, dxdt_name: str) -> None:
        self._x_name = x_name
        self._dxdt_name = dxdt_name
        self._object_adress = object_adress

    def x(self) -> float:
        return self._object_adress.__getattribute__(self._x_name)

    def set_x(self, x0: float) -> None:
        self._object_adress.__setattr__(self._x_name, x0)

    def dxdt(self) -> float:
        return self._object_adress.__getattribute__(self._dxdt_name)

    def variable_name(self) -> str:
        return f"{self._object_adress.name}:{self._x_name}:"


class solver:
    def __init__(self, object_function_names=["potential", "flux", "balance"]) -> None:
        self._objects = list()
        self._odes = list()
        self._object_function_names = object_function_names.copy()
        self._object_functions = {function_name: list() for function_name in object_function_names}

    def initialize(self):
        for object in self._objects:
            if "equations" in dir(object):
                for equation in object.equations:
                    if isinstance(equation, ode):
                        self._odes.append(equation)

        for object in self._objects:
            for function_name in self._object_function_names:
                if function_name in dir(object):
                    self._object_functions[function_name].append(object.__getattribute__(function_name))

    def integrate(self, tspan=[0, 1.0], method="RK45"):
        x0 = list()
        for edo in self._odes:
            x0.append(edo.x())
        if method in ("Radau", "BDF", "LSODA"):
            solution = solve_ivp(
                fun=self._edo_system,
                t_span=tspan,
                y0=x0,
                method=method,
                rtol=1.0e-8,
                jac=self._edo_system_derivative,
            )
        else:
            solution = solve_ivp(fun=self._edo_system, t_span=tspan, y0=x0, method=method, rtol=1.0e-8)

        variable_names = list()
        for edo in self._odes:
            variable_names.append(edo.variable_name())
        return solution.t, solution.y, variable_names

    def _compute_system(self):
        for function_name in self._object_function_names:
            for function in self._object_functions[function_name]:
                function()

    def _edo_system(self, t, y):
        for i_edo, edo in enumerate(self._odes):
            edo.set_x(y[i_edo])

        self._compute_system()
        v_dxdt = list()
        for i_edo, edo in enumerate(self._odes):
            dxdt = edo.dxdt()
            v_dxdt.append(dxdt)
        return v_dxdt

    def _edo_system_derivative(self, t, y):
        for i_edo, edo in enumerate(self._odes):
            edo.set_x(derivative(y[i_edo], i_edo))
        self._compute_system()
        N = len(self._odes)
        jacobian = [[0.0 for i in range(N)] for i in range(N)]
        for i_edo, edo in enumerate(self._odes):
            dxdt = edo.dxdt()
            for i_var in dxdt.diff.keys():
                jacobian[i_edo][i_var] = dxdt.val(i_var)
        for i_edo, edo in enumerate(self._odes):
            edo.set_x(y[i_edo])
        return jacobian


class object_base:
    def __init__(self, name: str) -> None:
        self.name = name
        self.equations = list()

    def add_ode(self, x_name: str, dxdt_name: str):
        self.equations.append(ode(object_adress=self, x_name=x_name, dxdt_name=dxdt_name))
