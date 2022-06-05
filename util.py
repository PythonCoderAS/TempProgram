def reverse_dict(dictionary):
    d = {}
    for key, values in dictionary.items():
        for value in values:
            d[value] = key
    return d