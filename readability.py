# Author: David B. Poot
# Filename: readability.py
# Date: 12/03/22
# Takes a text from cmd line and computes several readability scores
# from it such as "Brouwer Leesindex" and "ARI"

import sys
from nltk.tokenize import sent_tokenize, word_tokenize
import re


def split_clean_sent(text):
    """takes text as list and creates one string with all lines
    and returns a tokenized list"""
    lines = ""
    for line in text:
        lines += " "+line.strip()
    return sent_tokenize(lines)


def tokenize_clean(sents):
    """takes a list of sents and returns list of tokens in it"""
    words = list()
    for sent in sents:
        # tokenize each sentence
        sent_tokens = word_tokenize(sent)
        for token in sent_tokens:
            # add to words if not punctuation
            if token.isalnum():
                words.append(token)
    return words


def avg_char(wordlist):
    """takes list of words as input and returns average
    amount of chars per word as float"""
    word_cnt = len(wordlist)
    char_cnt = 0
    for word in wordlist:
        char_cnt += len(word)
    return (char_cnt/word_cnt)


def count_syl(wordlist):
    """takes list of words as input returns total of syllables in it as int"""
    syl_cnt = 0
    vowelgroups = "(aai|aa|au|a|eau|ee|ei|eu|e|ieu|ij|\
                    ie|i|ooi|oei|oe|ou|oo|o|ui|uu|u|y)"
    for word in wordlist:
        # cut words by all vowel groups and count the amount of parts that gives
        syl_cnt += len(re.findall(vowelgroups, word))
    return syl_cnt


def main():
    # get user input
    if(len(sys.argv) < 2):
        print("Please provide a text file: $ python3 \
               readability.py <text_file>")
        sys.exit(-1)
    else:
        with open(sys.argv[1], "r") as infile:
            text = infile.readlines()

    # compute text variables:
    sentences = split_clean_sent(text) # list: all tokenized sentences
    sent_cnt = len(sentences) # int: amount of sentences in text

    words = tokenize_clean(sentences) # list: all tokenized words
    word_cnt = len(words) # int: amount of words in text
    syllable_cnt = count_syl(words) # int: amount of syllables in text

    avg_sent_word = word_cnt/sent_cnt # float: average words per sentence
    avg_word_char = avg_char(words) # float: average characters per word
    avg_word_syll = syllable_cnt/word_cnt # float: average syllables per word

    # compute some readability scores
    brouwer_index = 195-(66.7*avg_word_syll)-(2*avg_sent_word)
    douma_score = 206.8-(77*avg_word_syll)-(0.93*avg_sent_word)
    ari_score = (4.71*avg_word_char)+(0.5*avg_sent_word)-21.43

    # print text info
    print("Sentences: {0}".format(sent_cnt))
    print("Words: {0}".format(word_cnt))
    print("Average Sentence Length: {0}".format(avg_sent_word))
    print("Average Word Length(char): {0}".format(avg_word_char))
    print("Average Word Length(syllables): {0}".format(avg_word_syll))
    print("\nBrouwer Leesindex: {0}".format(brouwer_index))
    print("Douma's score: {0}".format(douma_score))
    print("ARI score: {0}".format(ari_score))


if __name__ == "__main__":
    main()
