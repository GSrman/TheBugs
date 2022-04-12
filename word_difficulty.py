# Author: M. Elzinga
# Filename: word_difficulty
# Date: 15.03.2022
# Takes text file from terminal, outputs severals:
# list with difficult words and their amount,
# character count, paragraph count, indexes of double
# spaces and finds missing capitals at beginning of sentences

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


def check_spelling(text):
    '''takes text as str, returns list with possible spelling mistakes'''
    tok_lst = tokenize(text, 'nl')
    return [word for word in tok_lst if zipf_frequency(word, 'nl') == 0]


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
    '''finds missing capitals at start of sentence, returns list'''
    text = ' '.join(text.split('\n'))
    end = re.compile('([a-zA-Z]+[a-zA-Z][.!?] [a-z])')
    return end.findall(text)


def diff_words_html(text):
    '''replaces diff_words with a span element with class diff_words'''
    for word in find_difficult_words(text):
        text = text.replace(word, '<span class="diff_word">'+word+'</span>')
    return text


def mistake_check_html(text):
    '''replaces spell mistakes, non capitals and double spaces
    with span element with class mistake
    '''
    for word in check_spelling(text):
        text = text.replace(word, '<span class="mistake">'+word+'</span>')
    for no_cap in find_non_capitals(text):
        text = text.replace(no_cap, '<span class="mistake">'+no_cap+'</span>')
    return text.replace('  ', '<span class="mistake">  </span>')


def main():
    with open(sys.argv[1]) as infile:
        text = infile.read()

    diff_words = find_difficult_words(text)
    count_diff_words = len(diff_words)
    spelling_mistakes = check_spelling(text)

    spaces_index = find_spaces(text)
    char_count = count_char(text)
    par_count = count_par(text)
    no_capitals = find_non_capitals(text)

    print("List with difficult words({0}) \
        :\n{1}".format(count_diff_words, diff_words))
    print("\nList with indexes for double spaces:\n{0}".format(spaces_index))
    print("\nCharacter count: {0}".format(char_count))
    print("Paragraph count: {0}".format(par_count))
    print("\nIs there perhaps a capital \
        missing here?\n{0}".format(no_capitals))
    print("\nThese words possibly \
        contain a spelling mistake:\n{0}".format(spelling_mistakes))


if __name__ == '__main__':
    main()
