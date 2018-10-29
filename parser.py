import re
import sys
import os

DESTINATION_FOLDER = "to_process"
AGG_FOLDER = "aggr"
TAPE_FOLDER = "tape"



def check_if_line_is_first_part(line):

    if re.match("^\<\d\>", line):
        return True

    return False


def procces_line(line):
    line = line.replace("\n", "")

    matches = re.match("^\<\d\>.* (\/.*) MIDX.*L1-TAPE:(\d*:\d*).*\/(\/.*)", line)
    match1 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/AGG\..+)", line)
    match2 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/NON\..+)", line)
    match3 = re.match("^\<\d\>.* (\/.*) MIDX.*L1-TAPE:(\d*:\d*).*\/(\/.*)", line)

    file_name = matches.group(1)
    tape_number = (matches.group(2))
    NA_name = (matches.group(3))
    NON_AGG_name = (match2.group(3))

    # for aggregates, one file per aggregate with a list of all the files in that aggregate

    if match1:
        file_name = (match1.group(1))
        tape_number = (match1.group(2))
        AGG_name = (match1.group(3))

        #with open(DESTINATION_FOLDER + "/" + AGG_FOLDER + "/" + AGG_name, "a") as f:
        #    f.write(file_name + "\n")

        with open(DESTINATION_FOLDER + "/" + TAPE_FOLDER + "/" + tape_number  + "/" + AGG_name, "a") as f:
            f.write(file_name + "\n")

    # for non aggregates, all the files under the tape_name_NON directory
    if match2:
        file_name = (match2.group(1))
        tape_number = (match2.group(2))

        with open(DESTINATION_FOLDER + "/" + TAPE_FOLDER + "/" + tape_number + "_NON", "a") as f:
        f.write(file_name + "\n")

    #NON_AGG_name = (match2.group(3))



def update_console(count):
    sys.stdout.write("\rTotal lines checked: {}".format(count))
    sys.stdout.flush()


if __name__ == "__main__":

    filename = sys.argv[1]

    for folder in [AGG_FOLDER, TAPE_FOLDER]:
        path = DESTINATION_FOLDER + "/" + folder
        if not os.path.exists(path):
            os.makedirs(path)

    with open(filename) as infile:

        full_line = None

        count = 0
        for line in infile:
            if check_if_line_is_first_part(line):
                full_line = line
            if full_line is not None and not check_if_line_is_first_part(line):
                full_line = "{}{}".format(full_line, line)
                procces_line(full_line)
                count = count + 1
                update_console(count)
                full_line = None
