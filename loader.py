import base64
import sys
from os import listdir


def process_chunck(chunck_list):

    for tar in chunck_list:
        print(base64.b64decode(tar))

    print("\n")

if __name__ == "__main__":

    folder = sys.argv[1]
    offset = int(sys.argv[2])
    chunk = int(sys.argv[3])


    tape_list = [f for f in listdir(folder)]
    tape_list.sort()

    tape_list = tape_list[offset:offset+chunk]

    print(tape_list)
    #
    # chunck_list = []
    # total_tars = len(tar_list)
    # for index, tar in enumerate(tar_list, start=1):
    #
    #     chunck_list.append(tar)
    #     if index % chunck_size == 0 or index == total_tars:
    #         process_chunck(chunck_list)
    #         chunck_list = []




