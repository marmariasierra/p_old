import base64
import sys
import os
from os import listdir


def process_chunck(chunck_list):

    for tar in chunck_list:
        print(base64.b64decode(tar))

    print("\n")


if __name__ == "__main__":

    folder = sys.argv[1]
    offset = int(sys.argv[2])
    chunck = int(sys.argv[3])


    tape_list = [f for f in listdir(folder)]
    tape_list.sort()

    tape_list = tape_list[offset:offset+chunck]
    for line in tape_list:
        path= folder + "/" + line
        agg_list = listdir(path)
        for agg in agg_list:
            complete_name = folder + "/" + line + "/" + agg
            #number_agg = os.popen('wc -l ' + complete_name).read()
            #print(number_agg)
            os.system('more ' + complete_name)
            #more_cmd = 'more ' + complete_name
            #outcmd = os.system(more_cmd)
        #print(agg_list)

    #print(tape_list)





