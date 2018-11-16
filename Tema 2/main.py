import json
import math
import string

import load


def process_tfs(input):
    extra = {}

    for query, query_data in input.items():
        for url, doc in query_data.items():
            process_tfs_document(query.split(), doc)


def process_tfs_document(query, doc):
    L = doc['L']
    raw_scores = doc['raw_scores']
    raw_title = raw_scores['title']
    raw_header = raw_scores['header']
    raw_body = raw_scores['body']

    tfs = doc['tfs']
    tfs_title = tfs['title']
    tfs_header = tfs['header']
    tfs_body = tfs['body']

    for qw in query:
        if qw in raw_title:
            raw = raw_title[qw]
        else:
            raw = 0

        if raw == 0:
            tfs_title[qw] = 0
            continue

        tf = math.log10(raw)
        tf = 1 - tf
        tf = tf / L
        tfs_title[qw] = tf

    for qw in query:
        if qw in raw_header:
            raw = raw_header[qw]
        else:
            raw = 0

        if raw == 0:
            tfs_header[qw] = 0
            continue

        tf = math.log10(raw)
        tf = 1 - tf
        tf = tf / L
        tfs_header[qw] = tf

    for qw in query:
        if qw in raw_body:
            raw = raw_body[qw]
        else:
            raw = 0

        if raw == 0:
            tfs_body[qw] = 0
            continue

        tf = math.log10(raw)
        tf = 1 - tf
        tf = tf / L
        tfs_body[qw] = tf


'''
{
'query example': {
    url: {
        query_word: {
            tf_title: [1,1],
            tf_header: [1,1],
            tf_body: [1,1]
        } 
    }   
}
}
'''
#def create_vectors(input, res)


input = load.load_input()
process_tfs(input)
t = json.dumps(input, indent=4)
print(t[0:2000])
