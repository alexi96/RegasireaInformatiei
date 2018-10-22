import os
import sys
from sys import stdout

from merging import debug_to_merge

T = 9999999
DOCUMENTS_PATH = 'simple_test_data'  # 'real_data' or 'simple_test_data'
postList = {}
fileIds = {}

exclude_list = []  # ['in', 'the', 'and', 'a', 'of', 'to']
punctuation_string = "()[]{},.;@#'?!&$\"*"


def index_documents():
    for dirname, dirnames, filenames in os.walk(DOCUMENTS_PATH):
        id = 0
        for filename in filenames:
            path = os.path.join(dirname, filename)
            fileIds[path] = id
            index_file(path)
            id += 1
    sort_post()


# Apelat pt fiecare fisier
def index_file(path):
    index = 0
    with open(path, 'r') as f:
        for line in f:
            for word in line.split():
                if word in exclude_list:
                    continue

                index_token(word, fileIds[path], index)
                index += 1

    # pentru fiecare token din fisier apelam index token
    # obti un token din fisier
    # apelezi index_token(token, path, pozitia_tokenului_in_fisier)


def simple_tikenize(word):
    res = word
    res = ''.join(ch for ch in res if ch not in punctuation_string)

    if res.endswith('s'):  # Modifica pluralul in singularul res-ului
        res = res[:-1]

    res = res.lower()
    return res


# Apelat pt fiecare token din fisier
def index_token(token, file_id, index):
    #  newToken = re.sub(r"[,.;@#'?!&$]+\ *", "", token) # Scoate toate semnele de punctuatie
    token = simple_tikenize(token)

    if not token:  # daca e gol dupa prelucrare
        return
    if token in exclude_list:  # daca e gol dupa prelucrare
        return

    if token in postList:
        files = postList[token]
    else:
        files = {}
        postList[token] = files

    if file_id in files:
        position_list = files[file_id]
    else:
        position_list = []
        files[file_id] = position_list

    position_list.append(index)


def sort_post():
    for token, files in postList.items():
        for file, position_list in files.items():
            position_list.sort()


def print_post_list():
    for token, files in postList.items():
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
        q = simple_tikenize(q)
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


def merge_posting_list(query):

    to_merge = {}
    for q in query:
        to_merge[q] = postList[q]

    debug_to_merge(to_merge)

    while len(to_merge) > 1:
        t = iter(to_merge)
        first = next(t)
        second = next(t)

        t = merge_tow_post_lists(to_merge[first], to_merge[second])
        t = {(first + ' ' + second): t}

        del to_merge[first]
        del to_merge[second]

        to_merge = dict(t, **to_merge)
        debug_to_merge(to_merge)


index_documents()

#  print_post_list()

args = sys.argv
args = ['we', 'are', 'the']
query = tokenize_list(args)

merge_posting_list(query)
