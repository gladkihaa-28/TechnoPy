import difflib
from fuzzywuzzy import process


def find_most_similar(input_string, string_list):
    i = 1
    res = []
    try:
        while not res and i > 0:
            res = difflib.get_close_matches(input_string, string_list, cutoff=i)
            i -= 0.05
    except ValueError:
        pass

    if not res:
        i = 1
        res = []
        try:
            while not res and i > 0:
                res = difflib.get_close_matches(input_string.lower(), string_list, cutoff=i)
                i -= 0.05
        except ValueError:
            pass

    if not res:
        i = 1
        try:
            while not res and i > 0:
                res = difflib.get_close_matches(input_string.upper(), string_list, cutoff=i)
                i -= 0.05
        except ValueError:
            pass

    if not res:
        res = process.extract(input_string, string_list)
        res = [el[0] for el in res]

    return res