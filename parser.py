import re
import sys
import os
import base64

TAPE_FOLDER = "tapes"


def procces_line(line):
    line = line.replace("\n", "")

    match1 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/AGG\..+)", line)
    match2 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/NON\..+)", line)
    #match3 = re.match("^\<\d\>.* (\/.*) MIDX.*L1-TAPE:(\d*:\d*).*\/(\/.*)", line)

    match = None
    if match1:
        match = match1
    elif match2:
        match = match2

    if match:
        file_name = (match.group(1))
        tape_number = (match.group(2))

        path = TAPE_FOLDER + "/" + tape_number + "/"
        if not os.path.exists(path):
            os.makedirs(path)


        # for aggregates, one file per aggregate with a list of all the files in that aggregate

        if match1:
            AGG_name = base64.b64encode(match.group(3))
            with open(path + AGG_name, "a") as f:
                f.write(file_name + "\n")

        # for non aggregates, all the files under the tape_name_NON directory
        elif match2:
            with open(path + "NON", "a") as f:
                f.write(file_name + "\n")

        # else:
        #     with open(TAPE_FOLDER + "/" + tape_number + "/na", "a") as f:
        #         f.write(file_name + "\n")



def update_console(count):
    sys.stdout.write("\rTotal lines checked: {}".format(count))
    sys.stdout.flush()


if __name__ == "__main__":

    filename = sys.argv[1]

    with open(filename) as infile:

        full_line = None

        count = 0
        for line in infile:

            procces_line(line)
            count = count + 1
            update_console(count)
            full_line = None
