import base64
import sys
import os
from os import listdir


#def process_chunck(chunck_list):

#    for tar in chunck_list:
#        print(base64.b64decode(tar))
#
#    print("\n")



if __name__ == "__main__":

    folder = sys.argv[1]
    offset = int(sys.argv[2])
    chunck = int(sys.argv[3])

    os.system('sort tapes_list > tapes_list_sorted')

    #tape_list = tape_list_sorted[offset:offset+chunck]

    with open("tapes_list_sorted", "r") as f:
        for line in f:
            path = folder + "/" + line
            agg_list = []
            agg_list = os.popen('ls ' + path).read().split()
            for a in agg_list:
                complete_path = folder + "/" + str(line).strip() + "/" + a
                cmd = 'ghi_stage -f ' + complete_path + ' &'
                print(cmd)

#use f.readline() --> number of lines to read??
#use f.seeK(number of line) then f.read()

#from itertools import islice

# print the 100th line
#with open('the_file') as lines:
#    for line in islice(lines, 99, 100):
#        print line

#for n,line in enumerate(open("file")):
#    if n+1 in [26,30]: # or n in [25,29]
#       print line.rstrip()

#for i, line in enumerate(lines):

