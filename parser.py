import re
import sys
import os
import base64
import logging
from datetime import datetime
#import gzip

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
    LIST_FOLDER = "lists"
    count_lines = 0
    count_files = 0
    start_time = datetime.now()
    tapes_set = set()
    agg_set = set()
    non_set = set()
    path_lists = LIST_FOLDER + "/"
    os.makedirs(path_lists)


    def process_line(self, line):
        self.count_lines = self.count_lines + 1
        line = line.replace("\n", "")

        match1 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/AGG\..+)", line)
        match2 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/NON\..+)", line)
        #match1 = re.match("(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/AGG\.\S+)", line)
        #match2 = re.match("(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/NON\.\S+)", line)

        match = None
        if match1:
            match = match1
        elif match2:
            match = match2

        if match:
            file_name = match.group(1)
            tape_number = match.group(2)
            agg_name = match.group(3)


            path = self.TAPE_FOLDER + "/" + tape_number + "/"
            if not os.path.exists(path):
                os.makedirs(path)
                self.tapes_set.add(tape_number)


            # for aggregates, one file per aggregate with a list of all the files in that aggregate
            if match1:
                self.agg_set.add(agg_name)

                AGG_name = base64.b64encode(agg_name)
                with open(path + AGG_name, "a") as f:
                    f.write(file_name + "\n")
                    self.count_files = self.count_files + 1

            # for non aggregates, all the files under the tape_name_NON directory
            elif match2:
                self.non_set.add(file_name)

                with open(path + "NON", "a") as f:
                    f.write(file_name + "\n")

    def update_console(self):
        sys.stdout.write(
            "\rTotal lines checked: {0}, time elapased: {1}".format(self.count_lines, datetime.now() - self.start_time))
        sys.stdout.flush()

    def print_output(self):
        logger.info(
            "Total lines checked: {0} \nTotal tapes parsed: {1}. Total aggregates parsed: {2}. Total files in aggregates: {3}. "
            "Total non_aggregates parsed: {4}. Total elapsed time: {5} "
            .format(self.count_lines, len(self.tapes_set), len(self.agg_set), self.count_files, len(self.non_set),
                    datetime.now() - self.start_time))

    def create_lists(self):
        with open(self.LIST_FOLDER + "/tapes_list", "a") as f:
            f.write("\n".join(sorted(self.tapes_set)))

        with open(self.LIST_FOLDER + "/AGG_list", "a") as f:
            f.write("\n".join(self.agg_set))

        with open(self.LIST_FOLDER + "/NON_list", "a") as f:
            f.write("\n".join(self.non_set))

if __name__ == "__main__":

    #gzfile = sys.argv[1]
    filename = sys.argv[1]
    parser = Parser()

    with open(filename) as infile:
        for index, line in enumerate(infile):
        #for line in infile:
            parser.process_line(line)

            if index % 1000 == 0:
                parser.update_console()

    print("\n")
    parser.print_output()
    parser.create_lists()
