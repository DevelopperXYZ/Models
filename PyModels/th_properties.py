class properties:
    def __init__(self) -> None:
        pass

    def set_pt(self, P, T):
        raise (Exception("Must be defined"))

    def rho(self):
        raise (Exception("Must be defined"))

    def h(self):
        raise (Exception("Must be defined"))

    def drho_dp(self):
        raise (Exception("Must be defined"))

    def cp(self):
        raise (Exception("Must be defined"))


class water0_properties(properties):
    def __init__(self) -> None:
        # Water Properties around P = 1bar and T = 20°C (https://webbook.nist.gov/chemistry/fluid/)
        # Linear variations of specific enthalpy with T
        # Linear variations of density with P
        self._T_0 = 20.0  # °C
        self._P_0 = 1e5  # Pa
        self._h_0 = 84.0060539430e3  # J/kg
        self._rho_0 = 998.206543497  # kg/m3
        self._drho_dp_0 = 4.580939989797379e-07  # kg/m3/Pa
        self._cp_0 = 4.18405506707e03  # J/kg/K
        self._P = None  # Pressure (Pa)
        self._T = None  # Temperature (°C)

    def set_pt(self, P, T):
        """Set the pressure (Pa) and the temperature (°C)"""
        self._P = P
        self._T = T

    def rho(self):
        """P(Pa) returns rho in kg/m3"""
        return self._rho_0 + self._drho_dp_0 * (self._P - self._P_0)

    def h(self):
        """returns specific enthplpe in J/kg"""
        return self._h_0 + self._cp_0 * (self._T - self._T_0)

    def drho_dp(self):
        """returns derivative of density in kg/m3/Pa"""
        return self._drho_dp_0

    def cp(self):
        """returns specific heat capacity in J/kg/K"""
        return self._cp_0
