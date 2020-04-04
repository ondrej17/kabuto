import math
from scipy.special import sph_harm


class Descriptors:
    """
    class Descriptors
        > it can be changed to calculate whatever descriptors you choose, but
        > the function 'get_descriptors()' must return an array of floats
        > number of descriptors affects the neural network (# of its input nodes), so be careful
        > the function 'info_header' returns header for output file that contains descriptors
        >   ... it must be changed adequately
    """

    def __init__(self, id, x, y, z, atoms):
        self.id = id  # id of actual atom
        self.x, self.y, self.z = x, y, z  # coordination of actual atom
        self.r_min, self.r_max = self.set_r_min_max()  # set cutoff parameters
        self.atoms = self.create_atoms_in_cutoff(atoms)  # consider only atoms in cutoff

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

    def get_descriptors(self):
        """
        returns descriptors
            > it can be changed
            > it must returns an array of floats
            > number of descriptors affects the NN
        """
        return self.values_of_14_functions()

    def values_of_14_functions(self):
        """
        returns the list of 14 functions that describe a local structure for individual atom
            11 symmetry functions (G_2 and G_3 with different parameters)
            3 Steinhardt parameters (l = 6, 7, 8)
        """
        return [
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

            self.q_6(),
            self.q_7(),
            self.q_8()
        ]

    @staticmethod
    def set_r_min_max():
        """
        returns r_min and r_max in Angstroms
        """
        return 6.2, 6.4

    def f_c(self, r):
        """
        cutoff function, returns a value between 0 and 1
        'r' is distance between current atom and the other one, i. e. r_ij
        """
        if r <= self.r_min:
            return 1
        elif self.r_min < r <= self.r_max:
            return 0.5 + 0.5 * math.cos(math.pi * (r - self.r_min) / (self.r_max - self.r_min))
        elif self.r_max < r:
            return 0

    def g_2(self, r_s, eta):
        """
        symmetry function G_2
        it takes two parameters, eta and R_s
        """
        res = 0.
        for id, items in self.atoms.items():
            if id != self.id:  # exclude myself
                r_ij = math.sqrt((items[0] - self.x) ** 2 + (items[1] - self.y) ** 2 + (items[2] - self.z) ** 2)
                res += self.f_c(r_ij) * math.exp(-eta * (r_ij - r_s) ** 2)
        return res

    def g_3(self, kappa):
        """
        symmetry function G_3
        it takes one parameters, kappa
        """
        res = 0.
        for id, items in self.atoms.items():
            if id != self.id:  # exclude myself
                r_ij = math.sqrt((items[0] - self.x) ** 2 + (items[1] - self.y) ** 2 + (items[2] - self.z) ** 2)
                res += self.f_c(r_ij) * math.cos(kappa * r_ij)
        return res

    def q_6(self):
        """
        Steinhardt parameter with l = 6
        """
        l = 6
        res = 0
        for m in range(-l, l + 1, 1):
            res += abs(self.q_lm(l, m)) ** 2
        return math.sqrt(res * 4 * math.pi / (2 * l + 1))

    def q_7(self):
        """
        Steinhardt parameter with l = 7
        """
        l = 7
        res = 0
        for m in range(-l, l + 1, 1):
            res += abs(self.q_lm(l, m)) ** 2
        return math.sqrt(res * 4 * math.pi / (2 * l + 1))

    def q_8(self):
        """
        Steinhardt parameter with l = 8
        """
        l = 8
        res = 0
        for m in range(-l, l + 1, 1):
            res += abs(self.q_lm(l, m)) ** 2
        return math.sqrt(res * 4 * math.pi / (2 * l + 1))

    def q_lm(self, l, m):
        """
        returns value of function Q_lm
        """
        # numerator
        nom = 0
        for id, items in self.atoms.items():
            if id != self.id:  # exclude myself
                x_other, y_other, z_other = items[0], items[1], items[2]
                r_ij = math.sqrt((x_other - self.x) ** 2 + (y_other - self.y) ** 2 + (z_other - self.z) ** 2)
                nom += self.f_c(r_ij) * self.y_lm(l, m, x_other, y_other, z_other)
        # denominator
        den = 0
        for id, items in self.atoms.items():
            if id != self.id:  # exclude myself
                x_other, y_other, z_other = items[0], items[1], items[2]
                r_ij = math.sqrt((x_other - self.x) ** 2 + (y_other - self.y) ** 2 + (z_other - self.z) ** 2)
                den += self.f_c(r_ij)

        return nom / den

    def y_lm(self, l, m, x2, y2, z2):
        """
        returns value of spherical harmonics for given l and m
        [x2, y2, z2] are coordinates of other atom
        [self.x, self.y, self.z] are coordinates of current atom
        """
        # vector r_ij
        dx, dy, dz = self.x - x2, self.y - y2, self.z - z2

        # spherical coordinates of vector r_ij
        r = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        phi = math.atan2(dy, dx)
        theta = math.acos(dz / r)

        # return spherical harmonics
        return sph_harm(m, l, phi, theta)

    def create_atoms_in_cutoff(self, atoms):
        """
        creates a new dictionary, which contains only atoms that are in cutoff of current atom
        """
        res = dict()
        for id, items in atoms.items():
            r_ij = math.sqrt((items[0] - self.x) ** 2 + (items[1] - self.y) ** 2 + (items[2] - self.z) ** 2)
            if r_ij < self.r_max:
                res[id] = items
        return res

    @staticmethod
    def info_header(timestep, phase):
        """
        returns informative header that is to be written at the beginning of file with descriptors
        """
        return "# timestep {}\n" \
               "# phase {}\n" \
               "# id f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 f13 f14\n".format(timestep, phase)

# TODO: calculation of descriptors takes tool long, I must shorten it
# TODO: all function must be tested whether they give proper output
