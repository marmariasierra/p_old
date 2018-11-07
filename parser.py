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
    LIST_FOLDER = "lists"
    count_lines = 0
    count_files = 0
    start_time = datetime.now()
    agg_set = set()
    non_set = set()
    path_lists = LIST_FOLDER + "/"
    output_dict = {}

    def process_line(self, line):
        self.count_lines = self.count_lines + 1
        line = line.replace("\n", "")

        match1 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/AGG\..+)", line)
        match2 = re.match("<\d>.H\s.+\s(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/NON\..+)", line)
        # match1 = re.match("(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/AGG\.\S+)", line)
        # match2 = re.match("(/.+)\sMIDX:\d.+L1-TAPE:(\d+).+(//.+/NON\.\S+)", line)

        match = None
        if match1:
            match = match1
        elif match2:
            match = match2

        if match:
            file_name = match.group(1)
            tape_number = match.group(2)
            agg_name = match.group(3)

            file_agg_name = ''
            if match1:
                self.agg_set.add(agg_name)
                file_agg_name = base64.b64encode(agg_name)
                self.count_files = self.count_files + 1

            elif match2:
                self.non_set.add(file_name)
                file_agg_name = 'NON'

            if not tape_number in self.output_dict.keys():
                self.output_dict.update({tape_number: {}})

            if file_agg_name in self.output_dict.get(tape_number).keys():
                self.output_dict[tape_number][file_agg_name].append(file_name)

            else:
                self.output_dict[tape_number].update({file_agg_name: [file_name]})

    def write_dict_to_files(self):
        logger.info("writing dict to files")

        tapes_number_list = self.output_dict.keys()
        for tape_number in tapes_number_list:

            tape_path = self.TAPE_FOLDER + "/" + tape_number
            if not os.path.exists(tape_path):
                os.makedirs(tape_path)

            agg_list = self.output_dict.get(tape_number)

            for encoded_agg_name, filename_list in agg_list.iteritems():
                with open(tape_path + "/" + encoded_agg_name, "a") as f:
                    f.write("\n".join(filename_list))

            self.output_dict.pop(tape_number)

    def update_console(self):
        sys.stdout.write(
            "\rTotal lines checked: {0}, time elapsed: {1}".format(self.count_lines, datetime.now() - self.start_time))
        sys.stdout.flush()

    def print_output(self):
        logger.info(
            "Total lines checked: {0} \nTotal tapes parsed: {1}. Total aggregates parsed: {2}. Total files in aggregates: {3}. "
            "Total non_aggregates parsed: {4}. Total elapsed time: {5} "
                .format(self.count_lines, len(self.output_dict.keys()), len(self.agg_set), self.count_files,
                        len(self.non_set),
                        datetime.now() - self.start_time))

    def create_lists(self):

        if not os.path.exists(self.path_lists):
            os.makedirs(self.path_lists)

        with open(self.LIST_FOLDER + "/tapes_list", "a") as f:
            f.write("\n".join(sorted(self.output_dict.keys())))

        with open(self.LIST_FOLDER + "/AGG_list", "a") as f:
            f.write("\n".join(self.agg_set))

        with open(self.LIST_FOLDER + "/NON_list", "a") as f:
            f.write("\n".join(self.non_set))


if __name__ == "__main__":

    filename = sys.argv[1]
    parser = Parser()

    with open(filename) as infile:
        for index, line in enumerate(infile):
            parser.process_line(line)

            if index % 20000 == 0:
                parser.update_console()

    print("\n")

    parser.print_output()
    parser.create_lists()

    parser.write_dict_to_files()
