"""
{
    'index': [
        {
            'pointer': int
            'freq': int
            'id': int # posting id
        }

        ...
    ]
    'data': '...word1word2...'
}
"""
from sys import stdout

dictionary = {
    'index': [],
    'data': bytearray(b'')
}


def get_index_by_pointer(pointer):
    index = dictionary['index']
    data = dictionary['data']
    res = [s for s in index if s['pointer'] >= pointer]
    if len(res) == 1:
        res = res[0]
        res['len'] = len(data) - pointer
        return res
    elif len(res) >= 2:
        next = res[1]
        res = res[0]
        res['len'] = next['pointer'] - pointer
        return res
    return []


def get_token_by_pointer(pointer):
    index = dictionary['index']
    data = dictionary['data']
    t = get_index_by_pointer(pointer)
    l = t['len']
    return data[pointer:l].decode()


def add_to_dict(token):
    index = dictionary['index']
    data = dictionary['data']
    ptr = 0
    data_len = len(data)

    for ind in index:
        ptr = ind['pointer']
        t = get_token_by_pointer(ptr)
        if t == token:
            res = get_index_by_pointer(ptr)
            res['freq'] += 1
            return res

    data += bytearray(token, 'utf8')
    new_index = {
        'pointer': data_len,
        'freq': 1
    }
    index.append(new_index)
    return new_index


#  {'token': {'fr': 5, 'id': 7}}
def to_dictionary(tokens):
    index = dictionary['index']
    data = dictionary['data']
    for t, td in tokens.items():
        pointer = len(data)
        data += bytearray(t, 'utf8')
        new_index = {
            'pointer': pointer,
            'freq': td['fr'],
            'id': td['id']
        }
        index.append(new_index)


def print_dict():
    index = dictionary['index']
    data = dictionary['data']
    for i in index:
        stdout.write(str(i['id']))
        stdout.write(', ')
        stdout.write(str(i['pointer']))
        stdout.write(', ')
        stdout.write(str(i['freq']))
        stdout.write("\n")
    stdout.write(data.decode("utf-8"))
    stdout.write("\n")


def debug():
    add_to_dict('test')
    add_to_dict('test')
    add_to_dict('test')
    add_to_dict('test2')


# debug()
print_dict()
