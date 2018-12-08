import json
import math
import string

from matplotlib.mlab import frange

import load
from vectors import mul, dot, vec, add


def process(input):
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
        if L == 0:
            tfs_title[qw] = 0
            continue

        if qw in raw_title:
            raw = raw_title[qw]
        else:
            raw = 1  ###

        if raw == 0:
            tfs_title[qw] = 0
            continue

        tf = math.log10(raw)
        tf = 1 - tf
        tf = tf / L
        tfs_title[qw] = tf

    for qw in query:
        if L == 0:
            tfs_header[qw] = 0
            continue

        if qw in raw_header:
            raw = raw_header[qw]
        else:
            raw = 1  ###

        if raw == 0:
            tfs_header[qw] = 0
            continue

        tf = math.log10(raw)
        tf = 1 - tf
        tf = tf / L
        tfs_header[qw] = tf

    for qw in query:
        if L == 0:
            tfs_body[qw] = 0
            continue

        if qw in raw_body:
            raw = raw_body[qw]
        else:
            raw = 1  ###

        if raw == 0:
            tfs_body[qw] = 0
            continue

        tf = math.log10(raw)
        tf = 1 - tf
        tf = tf / L
        tfs_body[qw] = tf

    del doc['raw_scores']


def calculate_n(input):
    res = {}

    for query, query_data in input.items():
        for url, doc in query_data.items():
            res[url] = 1

    return len(res)


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

    del doc['tfs']


def calculate_idfs(input, N):
    dfs = {}
    for query, query_data in input.items():
        qv = query.split()
        for q in qv:
            dfs[q] = {}

    for query, query_data in input.items():
        for url, doc in query_data.items():
            rs = doc['raw_scores']
            t = rs['title']
            for qw, raw in t.items():
                if qw in dfs:
                    dfs[qw][url] = 1
            t = rs['header']
            for qw, raw in t.items():
                if qw in dfs:
                    dfs[qw][url] = 1
            t = rs['body']
            for qw, raw in t.items():
                if qw in dfs:
                    dfs[qw][url] = 1

    res_t = dfs
    dfs = {}
    for q, urls in res_t.items():
        dfs[q] = len(urls)

    for query, query_data in input.items():
        qv = query.split()

        for url, doc in query_data.items():
            l = len(qv)
            idf = []
            for i in range(l):
                q = qv[i]
                dfq = dfs[q]
                if dfq == 0:
                    idf.append(0)
                else:
                    idf.append(math.log(N / dfq))

            doc['idf'] = idf


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
            t = add(t, tfb)  # ( ... )
            t = dot(t, doc['idf'])
            score = t

            doc['score'] = score


input = load.load_input()
N = calculate_n(input)
calculate_idfs(input, N)
process(input)

calculate_score(input, 1, 1, 1)

relevance = load.load_relevance()

t = json.dumps(input, indent=4)
print(t[0:2000])

t = json.dumps(relevance, indent=4)
print(t[0:2000])

min_diff = 9999
min = [min_diff, min_diff, min_diff]

step = 0.1
for wt in frange(0, 1, step):
    for wh in frange(0, 1, step):
        for wb in frange(0, 1, step):
            calculate_score(input, wt, wh, wb)
            diff = 0

            for query, docs in relevance.items():
                calc_docs = input[query]
                for doc, score in docs.items():
                    calc_score = calc_docs[doc]['score']
                    diff += abs(score - calc_score)

            if diff < min_diff:
                min_diff = diff
                min = [wt, wh, wb]
                print(min)
                print(diff)

