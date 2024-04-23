from pyfinite import ffield
from decompose_cap_pts import *


def hamming_weight(n):
    """
    Algorithm by Stephen Nutt and Prashant Kumar.
    :param n: The integer to calculate the binary weight of
    :return: Returns the number of ones in the binary representation of n
    """
    weight = 0
    while n:
        weight += 1
        n &= n - 1  # This clears the rightmost bit in n and only the rightmost bit (so we count each bit this way)
    return weight


def dot_product(u, v):
    """
    Computes the dot product of two vectors in \F_2^n
    :param u: The first vector
    :param v: The second vector
    :return: The dot product of u and v.
    """
    return hamming_weight(u & v) % 2


class VBF:
    def __init__(self, field, function, use_caching=True, apn=None, ab=None):
        self.field = field
        self.n = field.n
        self.function = function
        self.use_caching = use_caching
        if use_caching:
            self.cache = {}
        self.apn = apn
        self.ab = ab

    def apply_function(self, x):
        if self.use_caching:
            if x in self.cache:
                return self.cache[x]
            else:
                self.cache[x] = self.function(x)
                return self.cache[x]
        return self.function(x)

    def walsh_spectrum(self):
        to_return = set()
        for a in range(2 ** self.n):
            for b in range(1, 2 ** self.n):
                to_return.add(walsh(self, a, b, self.field))
        return to_return

    def is_apn(self):
        if self.apn is not None:
            return self.apn
        n = self.n
        for a in range(1, 2 ** n):
            sol_range = set()
            for x in range(0, 2 ** n):
                sol_range.add(self.apply_function(x) ^ self.apply_function(x ^ a))
            if len(sol_range) != 2 ** (n - 1):
                self.apn = False
                return False
        self.apn = True
        return True

    def is_ab(self):
        # AB functions cannot exist in even dimensions (Canteaut, Charpin, and Dobbertin, '99)
        if self.ab is not None:
            return self.ab
        n = self.n
        if n % 2 == 0:
            return False
        m = 2 ** ((n + 1) / 2)
        return self.walsh_spectrum() == {0, -m, m}

    def is_crooked(self):
        if self.apply_function(0) != 0:
            return False
        n = self.n
        for x in range(2 ** n):
            for y in range(2 ** n):
                for z in range(2 ** n):
                    if self.apply_function(x) ^ self.apply_function(y) ^ self.apply_function(z) ^ self.apply_function(
                            x ^ y ^ z) == 0:
                        return False
                    for a in range(1, 2 ** n):
                        if self.apply_function(x) ^ self.apply_function(y) ^ self.apply_function(
                                z) ^ self.apply_function(x ^ a) ^ self.apply_function(y ^ a) ^ self.apply_function(
                            z ^ a) == 0:
                            return False
        return True

    def is_permutation(self):
        output = set()
        for x in range(2 ** self.n):
            eval_at_x = self.apply_function(x)
            if eval_at_x in output:
                return False
            output.add(eval_at_x)
        return True

    def is_plateaued(self):
        for v in range(2 ** self.n):
            outputs = {walsh(self, u, v, self.field) for u in range(2 ** self.n)}
            if len(outputs) < 3 or (len(outputs) == 3 and 0 in outputs and min(outputs) == -max(outputs)):
                continue
            return False
        return True

    def all_component_functions_unbalanced(self):
        for v in range(1, 2 ** self.n):
            if walsh(self, 0, v, self.field) == 0:
                return False
        return True


class PowerVBF(VBF):
    """
    Represents a function F from GF(2^n) to itself of the form F(x) = x^d.
    This is known as a power vectorial Boolean function.
    """

    def __init__(self, exponent, field, use_caching=True, apn=None, ab=None):
        super().__init__(field, lambda x: field_exp(x, int(exponent), field), use_caching, apn, ab)
        self.exponent = int(exponent)

    def algebraic_degree(self):
        """
        Computes the algebraic degree of this function.
        Since this is a vectorial Boolean power function, the algebraic degree is the 2-weight of the exponent.
        :return: The algebraic degree of F.
        """
        return bin(self.exponent).count('1')

    def get_exponent(self):
        """
        Get d where F(x) = x^d.
        :return: The exponent of this power function.
        """
        return self.exponent

    def walsh_spectrum(self):
        # Since F is a power function, it suffices to compute for a =0,1 and b \neq 0
        # because W_F(a,b) = W_F(1, a^{-d} b) for a \neq 0.
        to_return = set()
        for a in range(2):
            for b in range(1, 2 ** self.n):
                to_return.add(walsh(self, a, b, self.field))
        return to_return

    def cyclotomic_equivalent(self, power_vbf_function):
        d1 = self.get_exponent()
        d2 = power_vbf_function.get_exponent()
        n = self.n
        if math.gcd(d1, int(2 ** n) - 1) == 1:
            # This is the case when F is a permutation
            for i in range(n):
                if (d2 == (i * d1) % (int(2 ** n) - 1)
                        or (d1 * d2) % (int(2 ** n) - 1) == int(2 ** i)):
                    return True
        else:
            for i in range(n):
                if d2 == ((i * d1) % (int(2 ** n) - 1)):
                    return True

        return False


class OnePointChangeVBF(VBF):
    """
    This class represents a function F' obtained from a given function such that F' is obtained
    by changing the value of F at a single point.
    """

    def __init__(self, field, vbf_to_modify, input_to_change, translate_by):
        # F'(x) = F(x) + a if x = x_0
        # F'(x) = F(x) otherwise
        super().__init__(field,
                         lambda x:
                         vbf_to_modify.apply_function(x) if x != input_to_change
                         else vbf_to_modify.apply_function(x) ^ translate_by)


class BooleanFunction(VBF):
    def __init__(self, field, function):
        super().__init__(field, function)

    def is_bent(self):
        pass


def field_exp(x, exp, field):
    '''
    Computes an exponential power. Runs in logarithmic time.
    :param x: the base of the exponent
    :param exp: the power to raise x to
    :param field: the field x belongs in
    :return: the result of x^{exp}
    '''

    # 'Fast' exponentiation (Wikipedia)
    # https://en.wikipedia.org/wiki/Exponentiation_by_squaring

    # Temporary Variables
    a = x
    n = exp  # n is the exponent, not the dimension of the field

    # Base Cases
    if a == 0:
        return 0
    if n < 0:
        a = field.Inverse(a)
        n = -n
    if n == 0:
        return 1

    # Exponentiation by squaring
    y = 1
    while n > 1:
        if n % 2 == 1:
            y = field.Multiply(a, y)
            n -= 1
        a = field.Multiply(a, a)
        n = n / 2
    return field.Multiply(a, y)


def compute_polynomial(x, c, x_powers, c_powers, field):
    """
    Computes a polynomial given P(x) = Sum[c^(a_i) x^(b_i)]
        where a_i is the ith entry of x_powers and b_i is the ith entry of c_powers
    :param x: The input to the polynomial
    :param c: Used to define coefficients of the polynomial. If primitive, c^d can be any element non-zero element
    :param x_powers: The powers of x to evaluate, the ith entry will correspond to the ith power of x
    :param c_powers: The powers of c to evaluate, the ith entry will correspond to the ith power of c
    :param field: The field that x and c belong to
    :return:
    """
    result = 0
    for x_power, c_power in zip(x_powers, c_powers):
        result ^= field.Multiply(field_exp(x, x_power, field), field_exp(c, c_power, field))
    return result


def find_primitive_element(field):
    """
    Finds a random primitive element of the field given
    :param field: The field to find a primitive element for
    :return: An element c such that <c^i> = \F_{2^n}^\ast.
    """
    for element in range(2, 2 ** field.n):
        if is_primitive(element, field):
            return element


def is_primitive(element, field):
    n = field.n
    powers = set()
    current_power = 1
    for _ in range(1, 2 ** n):
        powers.add(current_power)
        current_power = field.Multiply(current_power, element)
    return len(powers) == int(2 ** n) - 1


def trace(x, field, m=1):
    if x == 0:
        return 0
    sum = 0
    n = field.n
    assert n % m == 0
    for i in range((n // m - 1) * m + 1):
        exp = int(2 ** (i * m))
        sum ^= field_exp(x, exp, field)
    return sum


def walsh(vbf, u, v, field):
    sum = 0
    n = field.n
    for x in range(pow(2, n)):
        # exp = (abs_trace(field.Multiply(v, vbf.apply_function(x)), field)
        #        ^ abs_trace(field.Multiply(u, x), field))
        exp = dot_product(u, x) ^ dot_product(v, vbf.apply_function(x))
        sum += pow(-1, exp)
    return sum


def walsh_spectrum(vbf):
    field = vbf.field
    n = field.n
    to_return = set()
    for a in range(2 ** n):
        for b in range(1, 2 ** n):
            to_return.add(walsh(vbf, a, b, field))
    return to_return


def build_graph(vbf):
    """
    Builds the graph of the function F: F_{2^n} to F_{2^n}.
    The graph of a function F is defined to be the set of all ordered pairs (x,F(x)) for all x in F_{2^n}.
    :param F: The function.
    :param n: The dimension of the field F is over
    :return:
    """
    n = vbf.field.n
    to_return = []
    for p in range(int(2 ** n)):
        to_return.append(concatenate_binary_strings(p, vbf.apply_function(p), n))
    return to_return


def derivative(F, a):
    return lambda x: F.apply_function(x) ^ F.apply_function(x ^ a)


def eval_derivative(F, a, x):
    return derivative(F, a)(x)


def second_order_derivative(F, a, b):
    return lambda x: F.apply_function(x) ^ F.apply_function(x ^ a) ^ F.apply_function(x ^ b) ^ F.apply_function(
        x ^ a ^ b)


def delta(F, n, a, b):
    return sum(1 for x in range(2 ** n) if eval_derivative(F, a, x) == b)


def gamma(F, n, a, b):
    if a == 0:
        return 0
    return 1 if delta(F, n, a, b) > 0 else 0


def gamma_weight(F, n):
    weight = sum(gamma(F, n, a, b) for a in range(2 ** n) for b in range(2 ** n))
    return weight


def gamma_function_table(F, n):
    """
    Returns the two-dimensional array defined by A_{ab} = gamma_F(a,b).
    This is a quick way to check where the derivative has solutions repeatability
    :return: A lookup table for the gamma function of a function F
    """
    return [[gamma(F, n, a, b) for b in range(2 ** n)] for a in range(2 ** n)]


def delta_function_table(F, n):
    """
    Returns the two-dimensional array defined by A_{ab} = delta_F(a,b).
    This is a quick way to check the number of solutions repeatability
    :return: A lookup table for the delta function of a function F
    """
    return [[delta(F, n, a, b) for b in range(2 ** n)] for a in range(2 ** n)]


def inverse_element(field, x):
    """
    Returns the multiplicative inverse of x != 0
    :param field: The field x is in
    :param x: The nonzero element of field
    """
    assert x != 0
    return field.Inverse(x)
