def get_str_version(data):
    return f'{data[0]}.{data[1]}.{data[2]}'

def get_tuple_range_version(data):
    return [tuple(data[0]), tuple(data[1])]

def get_version_in_range(version, range):
    min = range[0]
    max = range[1]
    if version >= min and version <= max:
        return True 
    return False