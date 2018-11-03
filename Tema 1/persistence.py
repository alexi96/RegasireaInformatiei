
"""
base64 token
"""
import base64
import os

DATABASES_FOLDER = 'disk'


def to_file_name(token):
    token = bytes(token, 'utf8')
    database_name = base64.b64encode(token)
    database_name = database_name.decode('utf8')
    database_name = os.path.join(DATABASES_FOLDER, database_name)
    return database_name


def write_word(token, files):
    database_name = to_file_name(token)

    with open(database_name, 'w') as fp:
        for fileId, positions in files.items():
            fp.write(str(fileId))
            fp.write(':')
            for p in positions:
                fp.write(str(p))
                fp.write(',')
            fp.write('\n')


"""
    file: 1 2 3 4
    file2: 2 6 8 9
"""
def merge_word(token, files):
    database_name = to_file_name(token)

    if not os.path.isfile(database_name):
        write_word(token, files)
        return

    database_name_temp = database_name + '.temp'

    with open(database_name) as fp, open(database_name_temp, 'w') as tf:
        line = fp.readline()

        if not line:
            write_word(token, files)
            return

        files = dict(files)
        while line:
            line = line.strip()

            fileid_positions = line.split(':')
            fileid = fileid_positions[0]
            fileid = int(fileid)
            positions = fileid_positions[1].split(',')
            positions = [int(p) for p in positions if p]
            if fileid in files:
                positions_to_merge = files[fileid]
                positions = list(set(positions) | set(positions_to_merge))
                positions = sorted(positions)
                del files[fileid]

            tf.write(str(fileid))
            tf.write(':')
            for p in positions:
                tf.write(str(p))
                tf.write(',')
            tf.write('\n')
            line = fp.readline()

        for fileid, positions in files.items():  # bagam si ce nu era in fisier
            tf.write(str(fileid))
            tf.write(':')
            for p in positions:
                tf.write(str(p))
                tf.write(',')
            tf.write('\n')
        fp.close()
        tf.close()
    os.remove(database_name)
    os.rename(database_name_temp, database_name)


def database_merge_posting_list(posting_list):
    for token, file in posting_list.items():
        merge_word(token, file)


def get_by_token(token):
    database_name = to_file_name(token)

    res = {}

    if not os.path.isfile(database_name):
        return res

    files = {}
    with open(database_name) as fp:
        line = fp.readline()

        if not line:
            return res

        while line:
            line = line.strip()

            fileid_positions = line.split(':')
            fileid = fileid_positions[0]
            fileid = int(fileid)
            positions = fileid_positions[1].split(',')
            positions = [int(p) for p in positions if p]
            files[fileid] = positions
            line = fp.readline()
    res[token] = files
    return res


def save_postlist(post_list, file, fileNames):
    for token, files in post_list.items():
        file.write(token)
        file.write("\n")
        for file_id, position_list in files.items():
            file.write("\t" + fileNames[file_id] + ": ")

            for position in position_list:
                file.write(str(position))
                file.write(", ")

            file.write("\n")
    file.write("\n")