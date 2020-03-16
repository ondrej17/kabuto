import math
from scipy.special import sph_harm


class DescriptorsError(Exception): pass


class Descriptors:
    def __init__(self, id, x, y, z, atoms):
        self.atoms = atoms
        self.id = id
        self.x, self.y, self.z = x, y, z
        # dictionary of parameters for symmetry functions
        self.symmetry_functions_parameters = {
            1: [2.8, 20.0],  # r_s [Angstrom], eta [angstrom ^ -2]
            2: [3.2, 20.0],
            3: [4.4, 20.0],
            4: [4.8, 20.0],
            5: [5.0, 20.0],
            6: [5.3, 20.0],
            7: [5.7, 20.0],
            8: [6.0, 20.0],
            9: [3.5],  # kappa [angstrom ^ -1]
            10: [4.5],
            11: [7.0]
        }
        self.r_min, self.r_max = 6.2, 6.4  # angstrom

    def values_of_14_functions(self):
        return [
            # 11 symmetry functions
            self.g_2(self.symmetry_functions_parameters[1][0],
                     self.symmetry_functions_parameters[1][1]),
            self.g_2(self.symmetry_functions_parameters[2][0],
                     self.symmetry_functions_parameters[2][1]),
            self.g_2(self.symmetry_functions_parameters[3][0],
                     self.symmetry_functions_parameters[3][1]),
            self.g_2(self.symmetry_functions_parameters[4][0],
                     self.symmetry_functions_parameters[4][1]),
            self.g_2(self.symmetry_functions_parameters[5][0],
                     self.symmetry_functions_parameters[5][1]),
            self.g_2(self.symmetry_functions_parameters[6][0],
                     self.symmetry_functions_parameters[6][1]),
            self.g_2(self.symmetry_functions_parameters[7][0],
                     self.symmetry_functions_parameters[7][1]),
            self.g_2(self.symmetry_functions_parameters[8][0],
                     self.symmetry_functions_parameters[8][1]),
            self.g_3(self.symmetry_functions_parameters[9][0]),
            self.g_3(self.symmetry_functions_parameters[10][0]),
            self.g_3(self.symmetry_functions_parameters[11][0]),
            # 3 steinhardt parameters
            self.q_6(),
            self.q_7(),
            self.q_8()
        ]

    # cutoff function
    def f_c(self, r):
        if r <= self.r_min:
            return 1
        elif self.r_min < r <= self.r_max:
            return 0.5 + 0.5 * math.cos(math.pi * (r - self.r_min) / (self.r_max - self.r_min))
        elif self.r_max < r:
            return 0
        else:
            print("ERROR: f_c")
            raise DescriptorsError

    # symmetry functions G_2
    def g_2(self, r_s, eta):
        res = 0.
        for id, items in self.atoms.items():
            if id != self.id:   # exclude myself
                r_ij = math.sqrt((items[0] - self.x) ** 2 + (items[1] - self.y) ** 2 + (items[2] - self.z) ** 2)
                res += self.f_c(r_ij) * math.exp(-eta * (r_ij - r_s) ** 2)
        return res

    # symmetry functions G_3
    def g_3(self, kappa):
        res = 0.
        for id, items in self.atoms.items():
            if id != self.id:   # exclude myself
                r_ij = math.sqrt((items[0] - self.x) ** 2 + (items[1] - self.y) ** 2 + (items[2] - self.z) ** 2)
                res += self.f_c(r_ij) * math.cos(kappa * r_ij)
        return res

    # steinhardt parameter (l = 6)
    def q_6(self):
        l = 6
        res = 0
        for m in range(-l, l + 1, 1):
            res += abs(self.q_lm(l, m)) ** 2
        return math.sqrt(res * 4 * math.pi / (2 * l + 1))

    # steinhardt parameter (l = 7)
    def q_7(self):
        l = 7
        res = 0
        for m in range(-l, l + 1, 1):
            res += abs(self.q_lm(l, m)) ** 2
        return math.sqrt(res * 4 * math.pi / (2 * l + 1))

    # steinhardt parameter (l = 8)
    def q_8(self):
        l = 8
        res = 0
        for m in range(-l, l + 1, 1):
            res += abs(self.q_lm(l, m)) ** 2
        return math.sqrt(res * 4 * math.pi / (2 * l + 1))

    def q_lm(self, l, m):
        # nominator
        res = 0
        for id, items in self.atoms.items():
            if id != self.id:   # exclude myself
                x_other, y_other, z_other = items[0], items[1], items[2]
                r_ij = math.sqrt((x_other - self.x) ** 2 + (y_other - self.y) ** 2 + (z_other - self.z) ** 2)
                res += self.f_c(r_ij) * self.y_lm(l, m, x_other, y_other, z_other)

        # denominator
        tmp = 0
        for id, items in self.atoms.items():
            if id != self.id:   # exclude myself
                x_other, y_other, z_other = items[0], items[1], items[2]
                r_ij = math.sqrt((x_other - self.x) ** 2 + (y_other - self.y) ** 2 + (z_other - self.z) ** 2)
                tmp += self.f_c(r_ij)

        return res / tmp

    def y_lm(self, l, m, x2, y2, z2):
        # vector r_ij
        dx, dy, dz = self.x - x2, self.y - y2, self.z - z2

        # spherical coordinates of vector r_ij
        r = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        phi = math.atan2(dy, dx)
        theta = math.acos(dz / r)

        # return spherical harmonics
        return sph_harm(m, l, phi, theta)

# TODO: calculation of descriptors takes tool long, I must shorten it
# TODO: all function must be tested whether they give proper output
# TODO: add more description for function and more comments
