from numpy import exp, log, sqrt
from numpy import sin, cos, tan, arcsin, arccos, arctan
from numpy import sinh, cosh, tanh, arcsinh, arccosh, arctanh


class derivative:
    def __init__(self, value=0.0, indix=-1):
        self.value = value
        self.indix = indix
        if indix < 0:
            self.diff = {}
        else:
            self.diff = {indix: 1.0}

    def __str__(self):
        """Definition of print derivative"""
        res = str(self.value)
        for k in self.diff.keys():
            res += f" {self.diff[k]}<{k}>"
        return res

    def val(self, indix=-1):
        if indix < 0:
            return self.value
        else:
            if indix in self.diff:
                return self.diff[indix]
            else:
                return 0

    def __pos__(self):
        res = derivative(self.value)
        for indix in self.diff.keys():
            res.diff[indix] = self.diff[indix]
        return res

    def __neg__(self):
        res = derivative(-self.value)
        for indix in self.diff.keys():
            res.diff[indix] = -self.diff[indix]
        return res

    def __eq__(self, other):
        if isinstance(other, derivative):
            return self.value == other.value
        elif isinstance(other, float) or isinstance(other, int):
            return self.value == other
        else:
            raise (TypeError)

    def __ne__(self, other):
        if isinstance(other, derivative):
            return self.value != other.value
        elif isinstance(other, float) or isinstance(other, int):
            return self.value != other
        else:
            raise (TypeError)

    def __lt__(self, other):
        if isinstance(other, derivative):
            return self.value < other.value
        elif isinstance(other, float) or isinstance(other, int):
            return self.value < other
        else:
            raise (TypeError)

    def __le__(self, other):
        if isinstance(other, derivative):
            return self.value <= other.value
        elif isinstance(other, float) or isinstance(other, int):
            return self.value <= other
        else:
            raise (TypeError)

    def __gt__(self, other):
        if isinstance(other, derivative):
            return self.value > other.value
        elif isinstance(other, float) or isinstance(other, int):
            return self.value > other
        else:
            raise (TypeError)

    def __ge__(self, other):
        if isinstance(other, derivative):
            return self.value >= other.value
        elif isinstance(other, float) or isinstance(other, int):
            return self.value >= other
        else:
            raise (TypeError)

    def __add__(self, other):
        """Definition of operator + : derivative + {derivative,float,int}"""
        if isinstance(other, derivative):
            value = self.value + other.value
            indix = set(list(self.diff.keys()) + list(other.diff.keys()))
            result = derivative(value)
            for k in indix:
                result.diff[k] = 0.0
                if k in self.diff.keys():
                    result.diff[k] += self.diff[k]
                if k in other.diff.keys():
                    result.diff[k] += other.diff[k]
            return result
        elif isinstance(other, float) or isinstance(other, int):
            result = derivative(self.value)
            for k in self.diff.keys():
                result.diff[k] = self.diff[k]
            result.value += other
            return result
        else:
            raise (TypeError)

    def __sub__(self, other):
        """Definition of operator - : derivative - {derivative,float,int}"""
        if isinstance(other, derivative):
            value = self.value - other.value
            indix = set(list(self.diff.keys()) + list(other.diff.keys()))
            result = derivative(value)
            for k in indix:
                result.diff[k] = 0.0
                if k in self.diff.keys():
                    result.diff[k] += self.diff[k]
                if k in other.diff.keys():
                    result.diff[k] -= other.diff[k]
            return result
        elif isinstance(other, float) or isinstance(other, int):
            result = derivative(self.value)
            for k in self.diff.keys():
                result.diff[k] = self.diff[k]
            result.value -= other
            return result
        else:
            raise (TypeError)

    def __mul__(self, other):
        """Definition of operator * : derivative * {derivative,float,int}"""
        if isinstance(other, derivative):
            value = self.value * other.value
            indix = set(list(self.diff.keys()) + list(other.diff.keys()))
            result = derivative(value)
            for k in indix:
                result.diff[k] = 0.0
                if k in self.diff.keys():
                    result.diff[k] += self.diff[k] * other.value
                if k in other.diff.keys():
                    result.diff[k] += other.diff[k] * self.value
            return result
        elif isinstance(other, float) or isinstance(other, int):
            res = derivative(self.value * other)
            for k in self.diff.keys():
                res.diff[k] = self.diff[k] * other
            return res
        else:
            raise (TypeError)

    def __truediv__(self, other):
        """Definition of operator / : derivative / {derivative,float,int}"""
        if isinstance(other, derivative):
            value = self.value / other.value
            indix = set(list(self.diff.keys()) + list(other.diff.keys()))
            result = derivative(value)
            for k in indix:
                result.diff[k] = 0.0
                if k in self.diff.keys():
                    result.diff[k] += self.diff[k] * other.value
                if k in other.diff.keys():
                    result.diff[k] -= other.diff[k] * self.value
                result.diff[k] /= other.value * other.value
            return result
        elif isinstance(other, float) or isinstance(other, int):
            res = derivative(self.value / other)
            for k in self.diff.keys():
                res.diff[k] = self.diff[k] / other
            return res
        else:
            raise (TypeError)

    def __radd__(self, other):
        """Definition of operator + : {float,int}+derivative"""
        return self.__add__(other)

    def __rsub__(self, other):
        """Definition of operator - : {float,int}-derivative"""
        res = self.__sub__(other)
        res *= -1.0
        return res

    def __rmul__(self, other):
        """Definition of operator * : {float,int}*derivative"""
        return self.__mul__(other)

    def __rtruediv__(self, other):
        """Definition of operator / : {float,int}/derivative"""
        return derivative(other) / self

    def __pow__(self, e):
        return exp(e * log(self))

    def abs(self):
        value = self.value
        if value < 0.0:
            res = derivative(-value)
            for k in self.diff.keys():
                res.diff[k] = -self.diff[k]
        else:
            res = derivative(value)
            for k in self.diff.keys():
                res.diff[k] = self.diff[k]
        return res

    def exp(self):
        value = exp(self.value)
        res = derivative(value)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * value
        return res

    def log(self):
        value = log(self.value)
        res = derivative(value)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] / self.value
        return res

    def sqrt(self):
        value = sqrt(self.value)
        res = derivative(value)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] / 2.0 / value
        return res

    def sin(self):
        value = sin(self.value)
        res = derivative(value)
        dres = cos(self.value)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def cos(self):
        value = cos(self.value)
        res = derivative(value)
        dres = -sin(self.value)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def tan(self):
        value = tan(self.value)
        res = derivative(value)
        dres = 1 + value**2
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def arcsin(self):
        value = arcsin(self.value)
        res = derivative(value)
        dres = 1.0 / sqrt(1.0 - self.value**2)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def arccos(self):
        value = arccos(self.value)
        res = derivative(value)
        dres = -1.0 / sqrt(1.0 - self.value**2)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def arctan(self):
        value = arctan(self.value)
        res = derivative(value)
        dres = 1.0 / (1.0 + self.value**2)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def sinh(self):
        value = sinh(self.value)
        res = derivative(value)
        dres = cosh(self.value)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def cosh(self):
        value = cosh(self.value)
        res = derivative(value)
        dres = sinh(self.value)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def tanh(self):
        value = tanh(self.value)
        res = derivative(value)
        dres = 1.0 - value**2
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def arcsinh(self):
        value = arcsinh(self.value)
        res = derivative(value)
        dres = 1.0 / sqrt(1.0 + self.value**2)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def arccosh(self):
        value = arccosh(self.value)
        res = derivative(value)
        dres = 1.0 / sqrt(self.value**2 - 1.0)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res

    def arctanh(self):
        value = arctanh(self.value)
        res = derivative(value)
        dres = 1.0 / (1.0 - self.value**2)
        for k in self.diff.keys():
            res.diff[k] = self.diff[k] * dres
        return res
