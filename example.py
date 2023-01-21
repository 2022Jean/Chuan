def truncate_strings_in_nested_list(nested_list, max_length):
    truncated_list = []
    for item in nested_list:
        if type(item) == str:
            truncated_list.append(item[:max_length])
        elif type(item) == list:
            truncated_list.append(truncate_strings_in_nested_list(item, max_length))
    return truncated_list


def truncate_strings(a, min_length, max_length):
    if isinstance(a, str):
        return a[:max_length] if len(a) > max_length else a
    elif isinstance(a, list):
        return [truncate_strings(x, min_length, max_length) for x in a]
    elif isinstance(a, dict):
        return {k: truncate_strings(v, min_length, max_length) for k, v in a.items()}
    else:
        return a


a_list = ['afgergfgergdfger', ['bfgergfgergdfger', ['cfgergfgergdfger'], {'k1': '1243242', 'k2': '565645634534'}],
          {'k3': '35345346543453453534', 'k4': '4565464534534535'}]
b_list = truncate_strings(a_list, 5, 10)
# print(b_list)
#
# c_list = ['afgergfger', ['bfgergfger', ['cfgergfger'], {'k1': '1243242', 'k2': '5656456345'}], {'k3': '3534534654', 'k4': '4565464534'}]
c_dict = {'k3': '35345346543453453534', 'k4': '4565464534534535'}
d_dict = truncate_strings(c_dict, 0, 10)
print(d_dict)
