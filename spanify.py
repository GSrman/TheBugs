#
#
#
#

def add_span(dataname, data):
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
