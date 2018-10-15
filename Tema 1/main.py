import os
import sys
from sys import stdout

T = 9999999
DOCUMENTS_PATH = 'real_data'
postList = {}
fileIds = {}

exclude_list = ['in', 'the', 'and', 'a', 'of', 'to']


def index_documents():
    for dirname, dirnames, filenames in os.walk(DOCUMENTS_PATH):
        id = 0
        for filename in filenames:
            path = os.path.join(dirname, filename)
            fileIds[path] = id
            index_file(path)
            id += 1
    sort_post()


#Apelat pt fiecare fisier
def index_file(path):
    index = 0
    with open(path, 'r') as f:
        for line in f:
            for word in line.split():
                if word in exclude_list:
                    continue

                index_token(word, fileIds[path], index)
                index += 1
    #pentru fiecare token din fisier apelam index token
    #obti un token din fisier
    #apelezi index_token(token, path, pozitia_tokenului_in_fisier)


#Apelat pt fiecare token din fisier
def index_token(token, file_id, index):
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
        stdout.write(token)
        stdout.write("\n")
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


args = sys.argv
args = ['we', 'are']

index_documents()

print_post_list()

