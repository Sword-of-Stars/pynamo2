import itertools

def flatten(data: list):
    return list(itertools.chain.from_iterable(data))

def flatten_dict(data: dict):
    return list(itertools.chain(*data.values()))