# Author: M. Elzinga
# Filename: sent_length.py
# Date: 11.04.2022
# according to sentence length assigns a color,
# creates dictionary, key is the sentence, value the color

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
        if count_dct[sent] > 30:
            color_dct[sent] = 'red'
        elif count_dct[sent] > 25:
            color_dct[sent] = 'orange'
        elif count_dct[sent] > 20:
            color_dct[sent] = 'yellow'
        else:
            color_dct[sent] = 'white'
    return color_dct


def dct_to_html(text_lst):
    '''
    from text list (readlines()),
    returns list with the sentences in an html span with a color
    as class. (red, orange, yellow, white)
    '''
    dct = dct_sent_len(text_lst)
    html_lst = ['<span class="'+dct[sent]+'">'+sent+'</span>' for sent in dct]
    return html_lst


def main():
    with open(sys.argv[1]) as infile:
        text_lst = infile.readlines()

    dct_color = dct_sent_len(text_lst)
    lst_html = dct_to_html(text_lst)

    print('Dictionary with sentences and a color \
        according to their length:\n{0}'.format(dct_color))
    print('List with sentences in html:\n{0}'.format(lst_html))


if __name__ == "__main__":
    main()
