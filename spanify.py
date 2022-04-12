# File: spanify.py
# Author: David B. Poot
# Date: 12/04/22
# Description: custom module that adds a span with a class
# based on values to an element and returns it again.

def add_span(dataname, data):
    """takes dataname as string and its value as number, then 
    based on the dictionary returns the data in a span with a 
    given class for HTML.
    """
    span_dict = {
        "par_rare_word": (10, 7, 4),
        "par_words": (100, 75, 50),
        "par_sents": (16, 12, 4),
        "word_char": (18, 15, 12),
        "word_syll": (6, 5, 4),
        "sent_word": (26, 22, 18) 
    }
    if data >= span_dict[dataname][0]:
        return "<span class='red'>"+str(data)+"</span"
    elif data >= span_dict[dataname][1]:
        return "<span class='orange'>"+str(data)+"</span"
    elif data >= span_dict[dataname][2]:
        return "<span class='yellow'>"+str(data)+"</span"
    else:
        return str(data)
