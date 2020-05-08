import math
import logging
from scipy.special import sph_harm

# create logger
logger = logging.getLogger('kabuto.descriptors')


class Descriptors:
    """
    class Descriptors
        > it can be changed to calculate whatever descriptors you choose, but
        > the function 'get_descriptors()' must return an array of floats
        > number of descriptors affects the neural network (# of its input nodes), so be careful
        > the function 'info_header' returns a header for the output file that contains descriptors
        > ... it must be changed adequately
        > class attribute 'number_of_descriptors' holds the number of descriptors
        > r_min and r_max are different for Steinhardt parameters and symmetry functions!
        > 'atoms_with_pbc' holds all atoms and their copies in all direction due to the PBC
    """
    # important class attribute; update it, when descriptors are changed
    number_of_descriptors = 14

    def __init__(self, id, x, y, z, atoms_with_pbc):
        self.id = id  # id of actual atom
        self.x, self.y, self.z = x, y, z  # coordination of actual atom
        self.atoms_for_g = self.create_atoms_in_cutoff_for_g_functions(atoms_with_pbc)
        self.atoms_for_q = self.create_atoms_in_cutoff_for_q_functions(atoms_with_pbc)

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
    def f_c(r, r_min, r_max):
        """
        cutoff function, returns a value between 0 and 1
            'r' is distance between current atom and the other one, i. e. r_ij
        """
        if r <= r_min:
            return 1.0
        elif r_min < r <= r_max:
            return 0.5 + 0.5 * math.cos(math.pi * (r - r_min) / (r_max - r_min))
        elif r_max < r:
            return 0.0

    def g_2(self, r_s, eta):
        """
        symmetry function G_2
        it takes two parameters, eta and R_s
        """
        r_min, r_max = self.set_r_min_max_g_functions()
        res = 0.
        for id, items in self.atoms_for_g.items():
            if id != self.id:  # skip myself
                r_ij = math.sqrt(math.pow(items[0] - self.x, 2) +
                                 math.pow(items[1] - self.y, 2) +
                                 math.pow(items[2] - self.z, 2))
                res += self.f_c(r_ij, r_min, r_max) * math.exp(-eta * math.pow(r_ij - r_s, 2))
        return res

    def g_3(self, kappa):
        """
        symmetry function G_3
        it takes one parameters, kappa
        """
        r_min, r_max = self.set_r_min_max_g_functions()
        res = 0.
        for id, items in self.atoms_for_g.items():
            if id != self.id:  # exclude myself
                r_ij = math.sqrt(math.pow(items[0] - self.x, 2) +
                                 math.pow(items[1] - self.y, 2) +
                                 math.pow(items[2] - self.z, 2))
                res += self.f_c(r_ij, r_min, r_max) * math.cos(kappa * r_ij)
        return res

    def q_6(self):
        """
        Steinhardt parameter with l = 6
        """
        l_param = 6
        res = 0
        for m in range(-l_param, l_param + 1, 1):
            res += math.pow(abs(self.q_lm(l_param, m)), 2)
        return math.sqrt(res * 4 * math.pi / (2 * l_param + 1))

    def q_7(self):
        """
        Steinhardt parameter with l = 7
        """
        l_param = 7
        res = 0
        for m in range(-l_param, l_param + 1, 1):
            res += math.pow(abs(self.q_lm(l_param, m)), 2)
        return math.sqrt(res * 4 * math.pi / (2 * l_param + 1))

    def q_8(self):
        """
        Steinhardt parameter with l = 8
        """
        l_param = 8
        res = 0
        for m in range(-l_param, l_param + 1, 1):
            res += math.pow(abs(self.q_lm(l_param, m)), 2)
        return math.sqrt(res * 4 * math.pi / (2 * l_param + 1))

    def q_lm(self, l_param, m):
        """
        returns value of function Q_lm
        """
        r_min, r_max = self.set_r_min_max_q_functions()
        # numerator
        nom = 0
        for id, items in self.atoms_for_q.items():
            if id != self.id:  # exclude myself
                x_other, y_other, z_other = items[0], items[1], items[2]
                r_ij = math.sqrt(math.pow(x_other - self.x, 2) +
                                 math.pow(y_other - self.y, 2) +
                                 math.pow(z_other - self.z, 2))
                nom += self.f_c(r_ij, r_min, r_max) * self.y_lm(l_param, m, x_other, y_other, z_other)
        # denominator
        den = 0
        for id, items in self.atoms_for_q.items():
            if id != self.id:  # exclude myself
                x_other, y_other, z_other = items[0], items[1], items[2]
                r_ij = math.sqrt(math.pow(x_other - self.x, 2) +
                                 math.pow(y_other - self.y, 2) +
                                 math.pow(z_other - self.z, 2))
                den += self.f_c(r_ij, r_min, r_max)

        return nom / den

    def y_lm(self, l_param, m, x2, y2, z2):
        """
        returns value of spherical harmonics for given l and m
        [x2, y2, z2] are coordinates of other atom
        [self.x, self.y, self.z] are coordinates of current atom
        """
        # vector r_ij
        dx, dy, dz = self.x - x2, self.y - y2, self.z - z2

        # spherical coordinates of vector r_ij
        r = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2))
        phi = math.atan2(dy, dx)
        theta = math.acos(dz / r)

        # return real form spherical harmonics in form Y_lm
        #   sph_harm() returns Y_l^m --> wikipedia
        if m < 0:
            return (-1)**m * math.sqrt(2) * (sph_harm(abs(m), l_param, phi, theta)).imag
        elif m == 0:
            return sph_harm(0, l_param, phi, theta)
        elif m > 0:
            return (-1)**m * math.sqrt(2) * (sph_harm(m, l_param, phi, theta)).real

    def create_atoms_in_cutoff_for_g_functions(self, atoms):
        """
        creates a new dictionary, which contains only atoms that are in cutoff of current atom
            cutoff is for G functions (symmetry functions)
        """
        r_min, r_max = self.set_r_min_max_g_functions()
        res = dict()
        for id, items in atoms.items():
            r_ij = math.sqrt(math.pow(items[0] - self.x, 2) +
                             math.pow(items[1] - self.y, 2) +
                             math.pow(items[2] - self.z, 2))
            if r_ij < r_max:
                res[id] = items
        return res

    def create_atoms_in_cutoff_for_q_functions(self, atoms):
        """
        creates a new dictionary, which contains only atoms that are in cutoff of current atom
            cutoff is for Steinhardt parameters
        """
        r_min, r_max = self.set_r_min_max_q_functions()
        res = dict()
        for id, items in atoms.items():
            r_ij = math.sqrt(math.pow(items[0] - self.x, 2) +
                             math.pow(items[1] - self.y, 2) +
                             math.pow(items[2] - self.z, 2))
            if r_ij < r_max:
                res[id] = items
        return res

    @staticmethod
    def info_header(timestep, phase):
        """
        returns informative header that is to be written at the beginning of file with descriptors
        """
        if phase is not None:
            return "# timestep {}\n" \
                   "# phase {}\n" \
                   "# id f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 f13 f14\n".format(timestep, phase)
        else:
            return "# timestep {}\n" \
                   "# id f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 f13 f14\n".format(timestep)

    @staticmethod
    def set_r_min_max_q_functions():
        """
        return r_min and r_max for cutoff function for Steinhardt bond parameters q
            units = Angstroms
        """
        return 3.8, 4.0

    @staticmethod
    def set_r_min_max_g_functions():
        """
        return r_min and r_max for cutoff function for symmetry functions G_2 and G_3
            units = Angstroms
        """
        return 6.2, 6.4
