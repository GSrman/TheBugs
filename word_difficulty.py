# Author: M. Elzinga
# Filename: word_difficulty
# Date: 15.03.2022

# Takes text file from terminal, outputs severals:
# list with difficult words and their amount,
# character count, paragraph count, indexes of double
# spaces and finds missing capitals at beginning of sentences

import scipy as sp
from wordfreq import *
import sys
import re


def find_difficult_words(text):
    '''takes text as str, returns list with difficult words'''
    # how they tokenize the text in this module
    tok_lst = tokenize(text, 'nl')
    # zipf_frequency: gives human readable score, 0-10 (10 being more frequent)
    # score of 2 means it occurs once in 100 million
    return [word for word in tok_lst if zipf_frequency(word, 'nl') <= 2]


def find_spaces(text):
    '''takes text as str, return list with index of two spaces'''
    return [m.start() for m in re.finditer('  ', text)]


def count_char(text):
    '''takes text as str, returns char count as int'''
    return len("".join(text.split("\n")))


def count_par(text):
    "takes text as str, returns int of amount of paragraphs"
    par_lst = [item for item in text.split("\n") if "." in item]
    return len(par_lst)


def find_non_capitals(text):
    text = ' '.join(text.split('\n'))
    end = re.compile('([a-zA-Z]+[a-zA-Z][.!?] [a-z])')
    return end.findall(text)


def main():
    with open(sys.argv[1]) as infile:
        text = infile.read()

    diff_words = find_difficult_words(text)
    count_diff_words = len(diff_words)
    
    spaces_index = find_spaces(text)
    char_count = count_char(text)
    par_count = count_par(text)
    no_capitals = find_non_capitals(text)

    print("List with difficult words({0}):\n{1}".format(count_diff_words, diff_words))
    print("\nList with indexes for double spaces:\n{0}".format(spaces_index))
    print("\nCharacter count: {0}".format(char_count))
    print("Paragraph count: {0}".format(par_count))
    print("\nIs there perhaps a capital missing here?\n{0}".format(no_capitals))


if __name__ == '__main__':
    main()
