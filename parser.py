import base64
import re
import sys
import os

DESTINATION_FOLDER = "archive"
TAR_FOLDER = "tar"
TAPE_FOLDER = "tape"


def check_if_line_is_first_part(line):

    if re.match("^\<\d\>", line):
        return True

    return False


def procces_line(line):
    line = line.replace("\n", "")

    matches = re.match("^\<\d\>.* (\/.*) MIDX.*L1-TAPE:(\d*:\d*).*\/(\/.*)", line)

    file_name = matches.group(1)

    tape_number = base64.b64encode(matches.group(2))

    tar_name = base64.b64encode(matches.group(3))

    with open(DESTINATION_FOLDER + "/" + TAR_FOLDER + "/" + tar_name, "a") as f:
        f.write(file_name + "\n")

    with open(DESTINATION_FOLDER + "/" + TAPE_FOLDER + "/" + tape_number, "a") as f:
        f.write(file_name + "\n")


def update_console(count):
    sys.stdout.write("\rTotal lines checked: {}".format(count))
    sys.stdout.flush()


if __name__ == "__main__":

    filename = sys.argv[1]

    for folder in [TAR_FOLDER, TAPE_FOLDER]:
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
