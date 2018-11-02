import os
import pickle
import sys
from sys import stdout

import compressing
from compressing import add_to_dict

T = 9999999
DOCUMENTS_PATH = 'simple_test_data'  # 'real_data' or 'simple_test_data'
postList = {}
fileIds = {}
fileNames = {}

exclude_list = []  # ['in', 'the', 'and', 'a', 'of', 'to']
punctuation_string = "()[]{},.;@#'?!&$\"*"


def index_documents():
    for dirname, dirnames, filenames in os.walk(DOCUMENTS_PATH):
        id = 0
        for filename in filenames:
            path = os.path.join(dirname, filename)
            fileIds[path] = id
            fileNames[id] = path
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


def simple_tokenize(word):
    res = word
    res = ''.join(ch for ch in res if ch not in punctuation_string)

    if res.endswith('s'):  # Modifica pluralul in singularul res-ului
        res = res[:-1]

    res = res.lower()
    return res


# Apelat pt fiecare token din fisier
def index_token(token, file_id, index):
    #  newToken = re.sub(r"[,.;@#'?!&$]+\ *", "", token) # Scoate toate semnele de punctuatie
    token = simple_tokenize(token)

    if not token:  # daca e gol dupa prelucrare
        return
    if token in exclude_list:  # daca e gol dupa prelucrare
        return

    # token is valid
    dictIndex = compressing.add_to_dict(token)
    #  tokenId = dictIndex['id']
    tokenId = token
    # add token to postlist
    if token in postList:
        files = postList[tokenId]
    else:
        files = {}
        postList[tokenId] = files

    if file_id in files:
        position_list = files[file_id]
    else:
        position_list = []
        files[file_id] = position_list

    position_list.append(index)


def sort_post():
    for token, files in postList.items():
        postList[token] = sort_files(files)


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


def merge_posting_list(query):
    res = {}
    for q in query:
        if q not in postList:
            return []
        res[q] = postList[q]

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


def save_to_disk(posting_list):
    SAVE_FILE = 'disk'
    file = open(SAVE_FILE, 'wb')
    pickle.dump(posting_list, file)
    file.close()


SAVE_FILE = 'disk'


def save_to_disk(posting_list):
    file = open(SAVE_FILE, 'wb')
    pickle.dump(posting_list, file)
    file.close()


def open_from_disk():
    file = open(SAVE_FILE, 'rb')
    res = pickle.load(file)
    file.close()
    return res


def debug_print(to_merge):
    for token, files in to_merge.items():
        stdout.write(token)
        stdout.write("\n")
        for file, position_list in files.items():
            stdout.write("\t" + fileNames[file] + ": ")

            for position in position_list:
                stdout.write(str(position))
                stdout.write(", ")

            stdout.write("\n")
    stdout.write("\n")


index_documents()

#  print_post_list()

args = sys.argv
args = ['a', 'file']  # ['we', 'are', 'the']
query = tokenize_list(args)
# query = compressing.to_posting_ids(query)

result = merge_posting_list(query)

debug_print(result)

#  save_to_disk(postList)
#  postList = open_from_disk()
#  debug_to_merge(postList)

compressing.print_dict()
