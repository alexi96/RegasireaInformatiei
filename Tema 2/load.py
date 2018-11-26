import os

INPUT_DATA = 'Training'
QUERY_DATA = 'queuries'
RELEVANCE_DATA = 'relevance'


'''
{
    'query example': {
        query: [query, example]
        documents: {
            'http://library.stanford.edu/': {
                L: 100
                raw_scores: {
                    title: {
                        query: 100
                        example: 100
                    },
                    header: {
                        query: 100
                        example: 100
                    },
                    body: {
                        query: 100
                        example: 100
                    }
                },
                tfs: {
                    title: {
                        query: 100
                        example: 100
                    },
                    headers: {
                        query: 100
                        example: 100
                    },
                    body: {
                        query: 100
                        example: 100
                    }
                }
            }
        }
    }
}
'''
def load_input():
    res = {}
    extra = {}

    path = os.path.join(INPUT_DATA, QUERY_DATA)
    with open(path, 'r', encoding="utf8") as f:
        for line in f:
            line = line.strip()
            words = line.split()
            if not words:
                continue
            load_line(words, res, extra)

    return res


def load_line(words, res, extra):
    first = words[0]
    first = ''.join(c for c in first if c not in ':')

    if first == 'query':
        load_query(words[1:], res, extra)
    elif first == 'url':
        load_url(words[1:], res, extra)
    elif first == 'title':
        load_title(words[1:], res, extra)
    elif first == 'header':
        load_header(words[1:], res, extra)
    elif first == 'body_hits':
        load_body_hits(words[1:], res, extra)
    elif first == 'body_length':
        load_body_length(words[1:], res, extra)


def load_query(query, res, extra):
    full_query = ' '.join(query)
    res[full_query] = {}
    extra['last_query'] = full_query


def load_url(url, res, extra):
    if not url:
        return

    url = url[0]
    last_query = extra['last_query']
    last = res[last_query]
    last[url] = {
        'L': 0,
        'raw_scores': {
            'title': {
            },
            'header': {
            },
            'body': {
            }
        },
        'tfs': {
            'title': {
            },
            'header': {
            },
            'body': {
            }
        },
        'tf_title_vector': [],
        'tf_header_vector': [],
        'tf_body_vector': []
    }
    extra['last_document'] = url


def in_query(word, query):
    return word in query
    nq = []
    for q in query:
        ln = round(len(q) / 4)
        if ln == 0:
            nq.append(q)
        else:
            nq.append(q[ln:-ln])

    res = [q for q in nq if q in word]
    res = len(res)
    return res > 0


def load_title(title_words, res, extra):
    last_query = extra['last_query']
    last_document = extra['last_document']
    last = res[last_query]

    query = last_query.split()

    last = last[last_document]
    raw_score = last['raw_scores']
    raw_score = raw_score['title']

    for tw in title_words:
        if not in_query(tw, query):
            continue

        if tw not in raw_score:
            raw_score[tw] = 0
        raw_score[tw] += 1

    last['L'] += len(title_words)


def load_header(header_words, res, extra):
    last_query = extra['last_query']
    last_document = extra['last_document']
    last = res[last_query]

    query = last_query.split()

    last = last[last_document]
    raw_score = last['raw_scores']
    raw_score = raw_score['header']

    for h in header_words:
        if not in_query(h, query):
            continue

        if h not in raw_score:
            raw_score[h] = 0
        raw_score[h] += 1

    last['L'] += len(header_words)


def load_body_hits(data, res, extra):
    if not data:
        return

    query_word = data[0]
    data = data[1:]

    last_query = extra['last_query']
    last_document = extra['last_document']
    last = res[last_query]
    last = last[last_document]
    raw_score = last['raw_scores']
    raw_score = raw_score['body']

    if query_word not in raw_score:
        raw_score[query_word] = 0
    raw_score[query_word] += len(data)


def load_body_length(data, res, extra):
    if not data:
        return
    data = data[0]

    last_query = extra['last_query']
    last_document = extra['last_document']
    last = res[last_query]
    last = last[last_document]

    last['L'] += int(data)

'''
{
query {
    url: score
}
}
'''
def load_relevance():
    res = {}
    extra = {}

    path = os.path.join(INPUT_DATA, RELEVANCE_DATA)
    with open(path, 'r', encoding="utf8") as f:
        for line in f:
            line = line.strip()
            words = line.split()
            if not words:
                continue
            load_relevance_line(words, res, extra)

    return res


def load_relevance_line(words, res, extra):
    first = words[0]
    first = ''.join(c for c in first if c not in ':')

    if first == 'query':
        load_relevance_query(words[1:], res, extra)
    elif first == 'url':
        load_relevance_url(words[1:], res, extra)


def load_relevance_query(query, res, extra):
    full_query = ' '.join(query)
    res[full_query] = {}
    extra['last_query'] = full_query


def load_relevance_url(url, res, extra):
    if not len(url) > 1:
        return

    score = url[1]
    url = url[0]

    last_query = extra['last_query']
    last = res[last_query]
    last[url] = score
