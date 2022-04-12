# Author: David B. Poot
# Filename: readability.py
# Date: 12/03/22
# Takes a text from cmd line and computes several readability scores
# from it such as "Brouwer Leesindex" and "ARI"

import sys
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import math


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


def count_chars(wordlist):
    """takes list of words as input and returns a tuple with total amount
    of chars as in, average amount of chars per word as float and list of words
    with more than 12 chars
    """
    word_cnt = len(wordlist)
    char_cnt = 0
    long_words = []
    for word in wordlist:
        word_char = len(word)
        if word_char > 12:
            long_words.append(word)
        char_cnt += word_char
    return char_cnt, (char_cnt/word_cnt), long_words


def count_syl(wordlist):
    """takes list of words as input returns total of syllables in it as int"""
    syl_cnt = 0
    long_words = []
    vowelgroups = "(aai|aa|au|a|eau|ee|ei|eu|e|ieu|ij|\
                    ie|i|ooi|oei|oe|ou|oo|o|ui|uu|u|y)"
    for word in wordlist:
        # cut words by all vowel groups and count the amount of parts
        word_syll_cnt = len(re.findall(vowelgroups, word))
        if word_syll_cnt > 4:
            long_words.append(word)
        syl_cnt += word_syll_cnt
    return syl_cnt, long_words


def get_long_sent(sentences):
    """"""
    extralong = []
    long = []
    vowelgroups = "(aai|aa|au|a|eau|ee|ei|eu|e|ieu|ij|\
                    ie|i|ooi|oei|oe|ou|oo|o|ui|uu|u|y)"
    for sent in sentences:
        sent_sylls = len(re.findall(vowelgroups, sent))
        if sent_sylls > 30:
            extralong.append(sent)
        elif sent_sylls > 20:
            long.append(sent)
    return extralong, long


def get_brouwerid(avg_word_syll, avg_sent_word):
    """takes average syllables per word and average words per sentence
       as number and returns brouwer index as float"""
    return 195-(66.7*avg_word_syll)-(2*avg_sent_word)


def get_douma(avg_word_syll, avg_sent_word):
    """takes average syllables per word and average words per sentence
       as number and returns douma score as float"""
    return 206.8-(77*avg_word_syll)-(0.93*avg_sent_word)


def get_ari(avg_word_char, avg_sent_word):
    """takes average characters per word and average words per sentence
       as number and returns ari score as float"""
    return (4.71*avg_word_char)+(0.5*avg_sent_word)-21.43


def get_avi(brouwer_index, avg_word_syll):
    """
    Takes number:[Brouwer-index] and returns int:[appropiate AVI level(1-9)]
    """
    if(127 >= brouwer_index >= 123):
        return 1
    # difference is determined in avg syllables because B.I. overlaps
    elif((123 >= brouwer_index >= 112) and (1.10 > avg_word_syll >= 1)):
        return 2
    elif((120 >= brouwer_index >= 108) and (1.15 > avg_word_syll >= 1.10)):
        return 3
    elif((110 >= brouwer_index >= 100) and (1.23 >= avg_word_syll >= 1.15)):
        return 4
    elif(99 >= brouwer_index >= 94):
        return 5
    elif(93 >= brouwer_index >= 89):
        return 6
    elif(88 >= brouwer_index >= 84):
        return 7
    elif(83 >= brouwer_index >= 79):
        return 8
    elif(78 >= brouwer_index):
        return 9


def get_edu(douma_score):
    """takes number:[douma-score] and returns string:[Associated
    Opleidings Niveau]"""
    if(100 >= douma_score >= 90):
        return "Groep 6 Basisschool"
    elif(90 > douma_score >= 80):
        return "Groep 7 Basisschool"
    elif(80 > douma_score >= 70):
        return "Groep 8 Basisschool"
    elif(70 > douma_score >= 60):
        return "Lager Middelbaar Onderwijs"
    elif(60 > douma_score >= 50):
        return "Hoger Middelbaar Onderwijs"
    elif(50 > douma_score >= 30):
        return "Studenten"
    elif(30 > douma_score):
        return "Academici"

def get_readlevel(avg_sent_word):
    """takes average amount of words per sentence as number and returns
        associated reading level
    """
    if avg_sent_word < 8:
        return "A1"
    elif avg_sent_word <= 10:
        return "A2"
    elif avg_sent_word <= 15:
        return "B1"
    elif avg_sent_word <= 20:
        return "B2"
    elif avg_sent_word <= 25:
        return "C1"
    else:
        return "C2"

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
    sentences = split_clean_sent(text)  # list: all tokenized sentences
    sent_cnt = len(sentences)  # int: amount of sentences in text

    words = tokenize_clean(sentences)  # list: all tokenized words
    word_cnt = len(words)  # int: amount of words in text
    syllable_cnt, long_words_syll = count_syl(words)  # int: total amount of syllables

    avg_sent_word = word_cnt/sent_cnt  # float: average words per sentence
    char_cnt, avg_word_char, long_words_char = count_chars(words)  # float: average characters per word
    avg_word_syll = syllable_cnt/word_cnt  # float: average syllables per word

    extra_long_sents, long_sents = get_long_sent(sentences)
    extra_long_sent_cnt = len(extra_long_sents)
    extra_long_sent_pct = math.floor(((extra_long_sent_cnt/sent_cnt)*100))
    long_sent_cnt = len(long_sents)
    long_sent_pct = math.floor(((long_sent_cnt/sent_cnt)*100))

    long_words_syll_cnt = len(long_words_syll)
    long_words_syll_pct = math.floor(((long_words_syll_cnt/word_cnt)*100))
    long_words_char_cnt = len(long_words_char)
    long_words_char_pct = math.floor(((long_words_char_cnt/word_cnt)*100))


    # compute some readability scores:

    # Leesindex R.H.M. Brouwer (1963)
    brouwer_index = get_brouwerid(avg_word_syll, avg_sent_word)

    # AnalyseVanIndividualiseringsvormen reading level
    avi_level = get_avi(brouwer_index, avg_word_syll)

    # Dutch adjusted Flesch score
    douma_score = get_douma(avg_word_syll, avg_sent_word)
    # Education level associated with Douma score
    edu_level = get_edu(douma_score)

    # Automated Readability Index
    ari_score = get_ari(avg_word_char, avg_sent_word)


    # print text info
    print("Sentences: {0}".format(sent_cnt))
    print("Words: {0}".format(word_cnt))

    print("\nAverage Sentence Length: {0}".format(avg_sent_word))
    print("Average Word Length(char): {0}".format(avg_word_char))
    print("Average Word Length(syllables): {0}".format(avg_word_syll))

    print("\nAmount of extra long sentences (syll>30): {0} ({1}%)".format(extra_long_sent_cnt, extra_long_sent_pct))
    print("Amount of long sentences (syll>20): {0} ({1}%)".format(long_sent_cnt, long_sent_pct))
    print("Amount of long words(syll>4): {0} ({1}%)".format(long_words_syll_cnt, long_words_syll_pct))
    print("Amount of long words(chars>12): {0} ({1}%)".format(long_words_char_cnt, long_words_char_pct))

    print("\nBrouwer Leesindex: {0}".format(brouwer_index))
    print("AVI level: {0}".format(avi_level))
    print("Douma's score: {0}".format(douma_score))
    print("Educatie-Level Douma Score: {0}".format(edu_level))
    print("ARI score: {0}".format(ari_score))


if __name__ == "__main__":
    main()
