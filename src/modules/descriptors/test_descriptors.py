import descriptors

# {atom_is:coordinates}
example_dict = {
    1: (0.5, 0.5, 10),
    2: (1.5, 6.3, 4.7),
    3: (6.1, 0.3, 4.1),
    4: (7.8, 8.3, 4.3),
    5: (0.9, 9.3, 4.4),
    6: (8.9, 3.0, 4.90),
    7: (0.8, 3.1, 4.12),
    8: (5.4, 3.6, 6.8),
    9: (5.3, 3.5, 9.8),
    10: (1.3, 3.4, 14.8)
}

# {pbc_x, pbc_y, pbc_z}
example_pbc = [1.2, 3.4, 5.0]

res = descriptors.compute(*example_pbc, example_dict)
print("\n\nPython code -->\n")
for key, value in res.items():
    print(key, " : ", value)

