import re
import sys
import os
import base64
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler("parser.log")
file_handler.setFormatter(formatter)

screen_handler = logging.StreamHandler()
screen_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(screen_handler)


class Parser:

    TAPE_FOLDER = "tapes"
    count_tape = 0
    count_agg =0
    count_aggfiles = 0
    count_non = 0
    count_lines = 0
    start_time = datetime.now()

    def process_line(self, line):
        self.count_lines = self.count_lines + 1
        line = line.replace("\n", "")

        match1 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/AGG\..+)", line)
        match2 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/NON\..+)", line)

        match = None
        if match1:
            match = match1
        elif match2:
            match = match2

        if match:
            file_name = (match.group(1))
            tape_number = (match.group(2))
            tapes_list= "tapes_list"
            path = self.TAPE_FOLDER + "/" + tape_number + "/"
            if not os.path.exists(path):
                os.makedirs(path)
                with open(tapes_list, "a") as f:
                    f.write(tape_number + "\n")
                self.count_tape = self.count_tape + 1

            # for aggregates, one file per aggregate with a list of all the files in that aggregate
            if match1:
                AGG_name = base64.b64encode(match.group(3))
                if not os.path.exists(path + AGG_name):
                    agg_list = "AGG_list"
                    with open(agg_list, "a") as f:
                        f.write(match.group(3) + "\n")
                    self.count_aggfiles = self.count_aggfiles + 1

                with open(path + AGG_name, "a") as f:
                    f.write(file_name + "\n")
                self.count_agg = self.count_agg + 1

            # for non aggregates, all the files under the tape_name_NON directory
            elif match2:
                non_list = "NON_list"
                with open(non_list, "a") as f:
                    f.write(file_name + "\n")
                with open(path + "NON", "a") as f:
                    f.write(file_name + "\n")
                self.count_non = self.count_non + 1



    def update_console(self):
        sys.stdout.write("\rTotal lines checked: {0}, time elapased: {1}".format(self.count_lines, datetime.now()-self.start_time))
        sys.stdout.flush()

    def print_output(self):
        logger.info("Total lines checked: {0} \nTotal tapes parsed: {1}. Total aggregates parsed: {2}. Total files in aggregates: {3}. "
                    "Total non_aggregates parsed: {4}. Total elapsed time: {5} "
                    .format(self.count_lines, self.count_tape, self.count_agg, self.count_aggfiles, self.count_non, datetime.now()-self.start_time ))


if __name__ == "__main__":

    filename = sys.argv[1]
    parser = Parser()

    with open(filename) as infile:
        for line in infile:
            parser.process_line(line)
            parser.update_console()

    print("\n")

    parser.print_output()
