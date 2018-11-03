import os
import pickle
import sys
from sys import stdout

import compressing
import persistence
from compressing import add_to_dict

T = 1000
DOCUMENTS_PATH = 'simple_test_data'  # 'real_data' or 'simple_test_data', 'disk_test_data'
fileIds = {}
fileNames = {}

exclude_list = []  # ['in', 'the', 'and', 'a', 'of', 'to']
punctuation_string = "()[]{},.;@#'?!&$\"*"


def index_documents():
    post_list = {}
    dictionary = {}  # {'token': {'fr': 5, 'id': 7}}

    for dirname, dirnames, filenames in os.walk(DOCUMENTS_PATH):
        id = 0
        for filename in filenames:
            path = os.path.join(dirname, filename)
            fileIds[path] = id
            fileNames[id] = path
            index_file(post_list, path, dictionary)
            id += 1

    #  sort_post(post_list)
    compressing.to_dictionary(dictionary)
    dictionary = None
    return post_list


# Apelat pt fiecare fisier
def index_file(post_list, path, dictionary):
    index = 0
    with open(path, 'r') as f:
        for line in f:
            for word in line.split():
                if word in exclude_list:
                    continue

                index_token(post_list, word, fileIds[path], index, dictionary)
                index += 1

                post_list_size = sys.getsizeof(post_list)
                if post_list_size >= T:
                    persistence.database_merge_posting_list(post_list)
                    post_list.clear()

    # pentru fiecare token din fisier apelam index token
    # obti un token din fisier
    # apelezi index_token(token, path, pozitia_tokenului_in_fisier)


def simple_tokenize(word):
    res = word
    res = ''.join(ch for ch in res if ch not in punctuation_string)

    if res.endswith('s'):  # Modifica pluralul in singularul res-ului
        res = res[:-1]

    res = res.lower()
    return res


# Apelat pt fiecare token din fisier
def index_token(post_list, token, file_id, index, dictionary):
    #  newToken = re.sub(r"[,.;@#'?!&$]+\ *", "", token) # Scoate toate semnele de punctuatie
    token = simple_tokenize(token)

    if not token:  # daca e gol dupa prelucrare
        return
    if token in exclude_list:  # daca e gol dupa prelucrare
        return

    # token is valid
    if token in dictionary:
        dictionary[token]['fr'] += 1
    else:
        dictionary[token] = {'id': len(dictionary), 'fr': 1}

    tokenId = token
    # add token to postlist
    if token in post_list:
        files = post_list[tokenId]
    else:
        files = {}
        post_list[tokenId] = files

    if file_id in files:
        position_list = files[file_id]
    else:
        position_list = []
        files[file_id] = position_list

    position_list.append(index)


def sort_post(post_list):
    for token, files in post_list.items():
        post_list[token] = sort_files(files)


def sort_files(files):
    files = files.copy()
    res = {}

    while len(files) > 0:
        max_obj = {}
        max_size = 0
        for file, position_list in files.items():
            l = len(position_list)
            if l > max_size:
                max_size = l
                max_obj = file
        res[max_obj] = files[max_obj]
        del files[max_obj]
    return res


def print_post_list(post_list):
    for token, files in post_list.items():
        stdout.write(token)
        stdout.write("\n")
        for file, position_list in files.items():
            stdout.write("\t" + str(file) + ": ")

            for position in position_list:
                stdout.write(str(position))
                stdout.write(", ")

            stdout.write("\n")
    stdout.write("\n")


def tokenize_list(query):
    res = []
    for q in query:
        q = simple_tokenize(q)
        res.append(q)
    return res


def merge_tow_post_lists(a, b):
    ak = []
    for key in a.keys():
        ak.append(key)

    bk = []
    for key in b.keys():
        bk.append(key)

    res = {}  # dictionar de fisiere
    keys = [value for value in ak if value in bk]  # lista cu id-urile comune ale fisierelor
    ai = 0
    bi = 1
    for k in keys:
        positions = [value for value in b[k] if (value - 1) in a[k]]
        if positions:
            res[k] = positions
    return res


def merge_posting_list(post_list, query):
    res = {}
    for q in query:
        if q not in post_list:
            return []
        res[q] = post_list[q]

    while len(res) > 1:
        t = iter(res)
        first = next(t)
        second = next(t)

        t = merge_tow_post_lists(res[first], res[second])
        t = {(first + ' ' + second): t}

        del res[first]
        del res[second]
        res = dict(t, **res)

    return res


def merge_posting_list_from_database(query):
    res = {}
    i = 0
    l = len(query)
    first = ''
    second = ''
    while i < l:
        if not res:
            n = query[i]
            res = persistence.get_by_token(n)
            if not res:
                return {}
            i += 1
            first = n
            continue

        second = query[i]
        i += 1

        t = persistence.get_by_token(second)
        if not t:
            return {}

        t = merge_tow_post_lists(res[first], t[second])
        del res[first]
        first = first + ' ' + second
        t = {first: t}
        res = dict(t, **res)
    return res


def debug_print(post_list):
    for token, files in post_list.items():
        stdout.write(token)
        stdout.write("\n")
        for file, position_list in files.items():
            stdout.write("\t" + fileNames[file] + ": ")

            for position in position_list:
                stdout.write(str(position))
                stdout.write(", ")

            stdout.write("\n")
    stdout.write("\n")


pl = index_documents()

#  print_post_list()

args = sys.argv
args = ['we', 'are', 'the']  # ['we', 'are', 'the']
query = tokenize_list(args)
# query = compressing.to_posting_ids(query)

result = merge_posting_list_from_database(query)
debug_print(result)

#  save_to_disk(postList)
#  postList = open_from_disk()
#  debug_to_merge(postList)

compressing.print_dict()
