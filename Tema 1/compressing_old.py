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
    'data': '...4word2to...'
}
"""
from sys import stdout

dictionary = {
    'index': [],
    'data': bytearray(b'')
}


# returns index value
def get_token_by_pointer(pointer):
    index = dictionary['index']
    data = dictionary['data']
    l = data[pointer]
    pointer += 1
    l += 1
    return data[pointer:l].decode()


def get_index_by_pointer(pointer):
    index = dictionary['index']
    res = [s for s in index if s['pointer'] == pointer]
    if res:
        return res[0]
    return []


def index_by_token(token):
    index = dictionary['index']
    data = dictionary['data']
    ptr = 0
    data_len = len(data)

    while ptr < data_len:
        t = get_token_by_pointer(ptr)
        if t == token:
            res = get_index_by_pointer(ptr)
            return res
        l = data[ptr]
        ptr += l

    return []


def add_to_dict(token):
    index = dictionary['index']
    data = dictionary['data']
    ptr = 0
    data_len = len(data)

    while ptr < data_len:
        t = get_token_by_pointer(ptr)
        if t == token:
            res = get_index_by_pointer(ptr)
            res['freq'] += 1
            return res
        l = data[ptr]
        ptr += l

    data.append(len(token))
    data += bytearray(token, 'utf8')
    new_index = {
        'pointer': data_len,
        'freq': 1,
        'id': len(index) + 1
    }
    index.append(new_index)
    return new_index


def to_posting_ids(tokens):
    res = []
    for t in tokens:
        ind = index_by_token(t)
        if ind:
           res.append(ind['id'])
    return res


def print_dict():
    index = dictionary['index']
    data = dictionary['data']
    for i in index:
        stdout.write(str(i['id']))
        stdout.write(': ')
        stdout.write(str(i['freq']))
        stdout.write(', ')
        stdout.write(str(i['pointer']))
        stdout.write("\n")
    stdout.write(data.decode("utf-8"))
    stdout.write("\n")


def debug():
    add_to_dict('test')
    add_to_dict('test')
    add_to_dict('test')
    add_to_dict('test2')


#debug()
#print_dict()
