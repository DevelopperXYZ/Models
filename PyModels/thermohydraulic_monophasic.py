from tools import sqrt_modif
from solver import object_base, solver
from th_properties import water0_properties


class thermohdraulic_connector:
    """Connections between objects"""

    def __init__(self) -> None:
        self.P = None  # Pressure (Pa)
        self.altitude = None  # Pressure (m)
        self.h = None  # Specific enthalpy (J/kg)
        self.rho = None  # Density (kg/m3)
        self.qm = None  # Mass flow (kg/s)
        self.qe = None  # Convected power (W)


class control_volume(object_base):
    """
    Modelisation of mass and energy balances :
        dm/dt = sum(qm)
        dh/dt = ( sum(qe) - h*sum(qm) ) / m
            - m  : mass (kg)
            - h  : specific enthalpy (J/kg)
            - qe : transorted power qe = h*qm (W)
            - qm : mass flow (kg/s)
        m = rho * V
            - rho : density (kg/m3)

    Approximations :
        dm/dt ~ V * (drho/dP)T * dP/dT
        dh/dt ~ (dh/dT)P * dT/dt = cp*dT/dT
            - cp : heat capacity at constant pressure (J/kg/K)
        dT/dt = (sum(qe) - h*qm) / (m * cp)
        dP/dt = sum(qm) / (V * (drho/dP)T)
    """

    def __init__(self, name: str, properties) -> None:
        # Initialize mother class
        super().__init__(name=name)
        self.properties = properties  # Object to compute fluid properties (h and rho)
        # Equations
        self._T = 20.0  # Temperature (°C)
        self._P = 1.0e5  # Pressure (Pa)
        self._dTdt = None
        self._dPdt = None
        self.add_ode("_T", "_dTdt")
        self.add_ode("_P", "_dPdt")
        # Parameters
        self.volume = 1.0  # m3
        self.altitude = 0.0  # m
        # Connections of objects which compute mass flow and convected power
        self.connections = list()
        # Internal variables
        self._h = None  # Specific enthalpy (J/kg)
        self._mass = None  # Mass (kg)

    def potential(self):
        self.properties.set_pt(self._P, self._T)
        rho = self.properties.rho()
        h = self.properties.h()
        for c in self.connections:
            c.P = self._P
            c.altitude = self.altitude
            c.h = h
            c.rho = rho
        self._h = h
        self._mass = rho * self.volume
        print(self, self._mass)

    def balance(self):
        qm_tot = 0.0
        qe_tot = 0.0
        for c in self.connections:
            qm_tot += c.qm
            qe_tot += c.qe
        self._dPdt = qm_tot / (self.volume * self.properties.drho_dp())
        self._dTdt = (1.0 / self.properties.cp()) * (qe_tot - self._h * qm_tot) / self._mass


class pressure_loss(object_base):
    """
    Object to modelise pressure loss
    qm = cv_qm * sqrt( rho * DP)
        - qm    : mass flow (kg/s)
        - cv_qm : hydraulic conductivity (m2)
        -
    """

    def __init__(self, name: str, cv_qm=1.0e-03) -> None:
        super().__init__(name)
        self._cv_qm = cv_qm  # Hydraulic conductivity (m2)
        self.qm = None  # Mass flow (kg/s)
        self.qe = None  # Convected power (W)
        self.cnx_1 = thermohdraulic_connector()  # Hydraulic conncection
        self.cnx_2 = thermohdraulic_connector()  # Hydraulic conncection

    def connect(self, volume_1, volume_2):
        volume_1.connections.append(self.cnx_1)
        volume_2.connections.append(self.cnx_2)

    def flux(self):
        dp = self.cnx_1.P - self.cnx_2.P
        if dp > 0:
            rho = self.cnx_1.rho
            h = self.cnx_1.h
        else:
            rho = self.cnx_2.rho
            h = self.cnx_2.h
        d_altitude = self.cnx_1.altitude - self.cnx_2.altitude
        dp += rho * 9.81 * d_altitude

        # sqrt_modif to avoid infinite derivative in 0
        dx_sqrt = 0.1
        qm = self._cv_qm * sqrt_modif(rho * dp, dx_sqrt)
        qe = h * qm

        self.qm = qm
        self.qe = qe

        self.cnx_1.qm = -qm
        self.cnx_1.qe = -qe

        self.cnx_2.qm = qm
        self.cnx_2.qe = qe
