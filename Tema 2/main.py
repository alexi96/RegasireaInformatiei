import json
import math
import string

import load
from vectors import mul, dot, vec, add


def process_tfs(input):
    extra = {}

    for query, query_data in input.items():
        for url, doc in query_data.items():
            qv = query.split()
            process_tfs_document(qv, doc)
            create_vectors(qv, doc)


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


def create_vectors(query, doc):
    tfs = doc['tfs']
    tfs_title = tfs['title']
    tfs_header = tfs['header']
    tfs_body = tfs['body']

    vec = []
    for qw in query:
        if qw not in tfs_title:
            vec.append(0)
        else:
            vec.append(tfs_title[qw])
    doc['tf_title_vector'] = vec

    vec = []
    for qw in query:
        if qw not in tfs_header:
            vec.append(0)
        else:
            vec.append(tfs_header[qw])
    doc['tf_header_vector'] = vec

    vec = []
    for qw in query:
        if qw not in tfs_body:
            vec.append(0)
        else:
            vec.append(tfs_body[qw])
    doc['tf_body_vector'] = vec


def calculate_score(input, wt, wh, wb):
    for query, query_data in input.items():
        for url, doc in query_data.items():
            qv = query.split()
            tft = doc['tf_title_vector']
            tfh = doc['tf_header_vector']
            tfb = doc['tf_body_vector']

            tft = mul(tft, wt)
            tfh = mul(tfh, wh)
            tfb = mul(tfb, wb)
            t = add(tft, tfh)
            t = add(t, tfb)

            score = dot(t, vec(1, len(t)))

            doc['score'] = score


input = load.load_input()
process_tfs(input)
calculate_score(input, 1, 1, 1)

relevance = load.load_relevance()

t = json.dumps(relevance, indent=4)
print(t[0:2000])
