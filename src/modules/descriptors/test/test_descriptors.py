import math
import descriptors
# from scipy.special import sph_harm


# def function_y_lm(l_param, m, dx, dy, dz):
#     # spherical coordinates of vector r_ij
#     r = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2))
#     phi = math.atan2(dy, dx)
#     theta = math.acos(dz / r)
#
#     # return real form spherical harmonics in form Y_lm
#     #   sph_harm() returns Y_l^m --> wikipedia
#     if m < 0:
#         return (-1) ** m * math.sqrt(2) * (sph_harm(abs(m), l_param, phi, theta)).imag
#     elif m == 0:
#         return sph_harm(0, l_param, phi, theta).real
#     elif m > 0:
#         return (-1) ** m * math.sqrt(2) * (sph_harm(m, l_param, phi, theta)).real


# print("Testing spherical harmonics in Python")
# print(function_y_lm(0, 0, 1, 1, 1))
# print(function_y_lm(0, 0, -1, -1, -1))
# print(function_y_lm(1, 1, 1, 1, 9))
# print(function_y_lm(1, 0, 1, 1, 9))
# print(function_y_lm(2, 0, 1, 1, 9))
# print(function_y_lm(2, 1, 1, 1, 9))
# print(function_y_lm(2, -1, 1, 1, 9))


# {atom_is:coordinates}
example_dict = {
    1: {1: (0.5, 0.5, 10),
        2: (1.5, 6.3, 4.7),
        3: (6.1, 0.3, 4.1)},
    2: {1: (0.5, 0.5, 10),
        2: (1.5, 6.3, 4.7),
        3: (6.1, 0.3, 4.1)},
    3: {1: (0.5, 0.5, 10),
        2: (1.5, 6.3, 4.7),
        3: (6.1, 0.3, 4.1)},
    4: {1: (0.5, 0.5, 10),
        2: (1.5, 6.3, 4.7),
        3: (6.1, 0.3, 4.1)}
}

# {pbc_x, pbc_y, pbc_z}
example_pbc = (1.2, 3.4, 5.0)

res = descriptors.compute(*example_pbc, example_dict)
print("\n\nPython code -->\n")
for key, value in res.items():
    print("timestep #", key, " : ")
    for key2, value2 in value.items():
        print("\tAtom #", key2, " : ", value2)
