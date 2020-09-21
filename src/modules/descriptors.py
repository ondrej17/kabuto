import math
import logging
from scipy.special import sph_harm

# set-up the logger
logger = logging.getLogger('kabuto.descriptors')


class Descriptors:
    """
    class Descriptors
        * it can be changed to calculate whatever descriptors you choose, but
        * the function 'get_descriptors()' must return an array of floats
        * number of descriptors affects the neural network (# of its input nodes), so be careful
        * the function 'info_header' returns a header for the output file that contains descriptors
        * ... it must be changed adequately
        * class attribute 'number_of_descriptors' holds the number of descriptors
        * r_min and r_max are different for Steinhardt parameters and symmetry functions!
        * 'all_atoms' holds all atoms in the simulation box
    """
    # important class attribute; update it, when descriptors are changed
    number_of_descriptors = 14

    def __init__(self, atom_id, x, y, z, all_atoms, pbc):
        self.atom_id = atom_id                                      # id of actual atom
        self.x, self.y, self.z = x, y, z                            # coordination of actual atom
        self.all_atoms = all_atoms                                  # all atoms in box
        self.pbc_x, self.pbc_y, self.pbc_z = pbc[0], pbc[1], pbc[2] # PBC

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
        for atom_id, items in self.all_atoms.items():
            if atom_id != self.atom_id:  # skip myself
                # vector r_ij
                x_ij = items[0] - self.x
                y_ij = items[1] - self.y
                z_ij = items[2] - self.z

                # correction of vector r_ij for PBC (and minimum image convention)
                x_ij -= self.pbc_x * round(x_ij / self.pbc_x)
                y_ij -= self.pbc_y * round(y_ij / self.pbc_y)
                z_ij -= self.pbc_z * round(z_ij / self.pbc_z)

                # calculate the correct length of vector r_ij
                r_ij = math.sqrt(math.pow(x_ij, 2) + math.pow(y_ij, 2) + math.pow(z_ij, 2))

                res += self.f_c(r_ij, r_min, r_max) * math.exp(-eta * math.pow(r_ij - r_s, 2))
        return res

    def g_3(self, kappa):
        """
        symmetry function G_3
        it takes one parameter, kappa
        """
        r_min, r_max = self.set_r_min_max_g_functions()
        res = 0.
        for atom_id, items in self.all_atoms.items():
            if atom_id != self.atom_id:  # skip myself
                # vector r_ij
                x_ij = items[0] - self.x
                y_ij = items[1] - self.y
                z_ij = items[2] - self.z

                # correction of vector r_ij for PBC (and minimum image convention)
                x_ij -= self.pbc_x * round(x_ij / self.pbc_x)
                y_ij -= self.pbc_y * round(y_ij / self.pbc_y)
                z_ij -= self.pbc_z * round(z_ij / self.pbc_z)

                # calculate the correct length of vector r_ij
                r_ij = math.sqrt(math.pow(x_ij, 2) + math.pow(y_ij, 2) + math.pow(z_ij, 2))

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
        num = 0
        for atom_id, items in self.all_atoms.items():
            if atom_id != self.atom_id:  # skip myself
                # vector r_ij
                x_ij = items[0] - self.x
                y_ij = items[1] - self.y
                z_ij = items[2] - self.z

                # correction of vector r_ij for PBC (and minimum image convention)
                x_ij -= self.pbc_x * round(x_ij / self.pbc_x)
                y_ij -= self.pbc_y * round(y_ij / self.pbc_y)
                z_ij -= self.pbc_z * round(z_ij / self.pbc_z)

                # calculate the correct length of vector r_ij
                r_ij = math.sqrt(math.pow(x_ij, 2) + math.pow(y_ij, 2) + math.pow(z_ij, 2))

                # addition to a numerator
                num += self.f_c(r_ij, r_min, r_max) * self.y_lm(l_param, m, x_ij, y_ij, z_ij)

        # denominator
        den = 0
        for atom_id, items in self.all_atoms.items():
            if atom_id != self.atom_id:  # skip myself
                # vector r_ij
                x_ij = items[0] - self.x
                y_ij = items[1] - self.y
                z_ij = items[2] - self.z

                # correction of vector r_ij for PBC (and minimum image convention)
                x_ij -= self.pbc_x * round(x_ij / self.pbc_x)
                y_ij -= self.pbc_y * round(y_ij / self.pbc_y)
                z_ij -= self.pbc_z * round(z_ij / self.pbc_z)

                # calculate the correct length of vector r_ij
                r_ij = math.sqrt(math.pow(x_ij, 2) + math.pow(y_ij, 2) + math.pow(z_ij, 2))

                # addition to a denominator
                den += self.f_c(r_ij, r_min, r_max)

        return num / den

    @staticmethod
    def y_lm(l_param, m, dx, dy, dz):
        """
        returns value of spherical harmonics for given l and m
        [dx, dy, dz] is a vector between two atoms
        [self.x, self.y, self.z] are coordinates of current atom
        """

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
