from sys import stdout


def debug_to_merge(to_merge):
    for token, files in to_merge.items():
        stdout.write(token)
        stdout.write("\n")
        for file, position_list in files.items():
            stdout.write("\t" + str(file) + ": ")

            for position in position_list:
                stdout.write(str(position))
                stdout.write(", ")

            stdout.write("\n")
    stdout.write("\n")
