
"""
base64 token
"""
import base64
import os

DATABASES_FOLDER = 'disk'


"""
    file: 1 2 3 4
    file2: 2 6 8 9
"""
def merge_word(token, files):
    database_name = base64.b64decode(token)
    database_name = os.path.join(DATABASES_FOLDER, database_name)
    database_name_temp = database_name + 'temp'

    file_index = 0

    with open(database_name) as fp, open(database_name_temp) as tf:
        line = fp.readline()
        while line:
            line = line.split()
            tf.write(line)
            tf.write(files[line[0]])

