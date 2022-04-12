# Author: M. Elzinga
# Filename: sent_length.py
# Date: 11.04.2022
# according to sentence length assigns a color,
# creates dictionary, key is the sentence, value the color

from re import S
from readability import split_clean_sent
import sys


def dct_sent_len(text_lst):
    '''
    from text list (readlines()),
    returns dictionary with colors as values and sentences as keys.
    Colors are according to sentence length
    '''
    sent_lst = split_clean_sent(text_lst)
    count_dct = {sent: len(sent.split(' ')) for sent in sent_lst}
    color_dct = {}
    for sent in sent_lst:
        if count_dct[sent] > 45:
            color_dct[sent] = 'red'
        elif count_dct[sent] > 35:
            color_dct[sent] = 'orange'
        elif count_dct[sent] > 25:
            color_dct[sent] = 'yellow'
        else:
            color_dct[sent] = 'white'
    return color_dct


def main():
    with open(sys.argv[1]) as infile:
        text_lst = infile.readlines()

    print(dct_sent_len(text_lst))


if __name__ == "__main__":
    main()
