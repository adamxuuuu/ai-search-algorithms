import json
import random
import string

import networkx as nx


def random_pass(stringLength=1):
    """
    function definition
    generate random password from 'Uppercase' '0-9' '_' of length 10
    """
    lettersAndDigits = string.ascii_uppercase + string.digits + "_"
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


def best_item_by_value(d):
    """
    return the best item in a dict
    by its value
    """
    v = list(d.values())
    k = list(d.keys())

    bst_idx = v.index(max(v))
    bst_key = k[bst_idx]
    return bst_key, d[bst_key]


def load_graph_from_file(filename):
    with open(filename) as f:
        d_f = json.load(f)
        return nx.Graph(d_f)

def find_idx(item, seq):
    """
    find the index of the item
    in iterable seq
    """
    for i, tpl in enumerate(seq):
        if tpl[1] == item:
            return i
    return None