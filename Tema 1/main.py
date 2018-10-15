import os
import sys

DOCUMENTS_PATH = 'real_data'
postList = {}


def index_documents():
    for dirname, dirnames, filenames in os.walk(DOCUMENTS_PATH):
        # print path to all filenames.
        for filename in filenames:
            path = os.path.join(dirname, filename)
            index_file(path)


#Apelat pt fiecare fisier
def index_file(path):
    print(path)
    # pentru fiecare token din fisier apelam index token
    #obti un token din fisier
    #apelezi index_token(token, path, pozitia_tokenului_in_fisier)


#Apelat pt fiecare token din fisier
def index_token(token, file, index):
    if token in postList:
        files = postList[token]
    else:
        files = {}

    files[file].append(index)


def print_post_list:
    print("Mai tarziu")

args = sys.argv
args = ['we', 'are']

for arg in sys.argv:
    index_documents()
