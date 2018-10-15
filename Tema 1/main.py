import os
import sys
from sys import stdout

DOCUMENTS_PATH = 'real_data'
postList = {}



def index_documents():
    for dirname, dirnames, filenames in os.walk(DOCUMENTS_PATH):
        # print path to all filenames.
        for filename in filenames:
            path = os.path.join(dirname, filename)
            index_file(path)
    sort_post()


#Apelat pt fiecare fisier
def index_file(path):
    index = 0
    with open(path, 'r') as f:
        for line in f:
            for word in line.split():
                index_token(word, path, index)
                index += 1

    # pentru fiecare token din fisier apelam index token
    #obti un token din fisier
    #apelezi index_token(token, path, pozitia_tokenului_in_fisier)



#Apelat pt fiecare token din fisier
def index_token(token, file, index):
    for i in range(32, 63):
        if token == i:
            str.Replace(token,"")
        if token.find(token,i):



    if token in postList:
        files = postList[token]
    else:
        files = {}
        postList[token] = files

    if file in files:
        position_list = files[file]
    else:
        position_list = []
        files[file] = position_list

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
            stdout.write("\t" + file + ": ")

            for position in position_list:
                stdout.write(str(position))
                stdout.write(", ")

            stdout.write("\n")
    stdout.write("\n")

args = sys.argv
args = ['we', 'are']

for arg in sys.argv:
    index_documents()

print_post_list()
