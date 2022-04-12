# File: timing.py
# Author: David B. Poot
# Date: 12/04/22
# Takes amount of words from cmd-line and returns the amount of time
# <min>:<sec> it would take to read and speak it.

import sys


def get_readtime(word_cnt):
    """Takes amount of words as number and returns an estimate time 
    it would take to read it as string: <min>:<sec>"""
    total_seconds = int(word_cnt // 3.75)+1
    remainder_seconds = str(total_seconds % 60)
    if len(remainder_seconds) == 1:
        remainder_seconds = "0"+remainder_seconds
    time = str(int(total_seconds//60))+":"+remainder_seconds
    return time

def get_speaktime(word_cnt):
    """Takes amount of words as number and returns an estimate time 
    it would take to speak it as string: <min>:<sec>"""
    total_seconds = int(word_cnt // 2.1)+1
    remainder_seconds = str(total_seconds % 60)
    if len(remainder_seconds) == 1:
        remainder_seconds = "0"+remainder_seconds
    time = str(int(total_seconds//60))+":"+remainder_seconds
    return time

def main():
    # get user input
    if(len(sys.argv) < 2):
        print("Please provide number of words: $ python3 \
               readability.py <n_words>")
        sys.exit(-1)
    else:
        word_cnt = int(sys.argv[1])

    print("Reading time of {0} is {1}".format(sys.argv[1], get_readtime(word_cnt)))
    print("Speaking time of {0} is {1}".format(sys.argv[1], get_speaktime(word_cnt)))

if __name__ == "__main__":
    main()
