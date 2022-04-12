# File: process.py
# Author: G.J.H. Schuurman
# Date: 12/04/2022
# The core: uses flask to render the webpage, and receives data to process,
# which it sents to and receives from the different required functions,
# and finally sends the required results back to the js file in json format.

from flask import Flask, render_template, request, jsonify
from readability import *
from timing import *
from word_difficulty import *
from sent_length import *


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('webpage.html')

@app.route('/process', methods=['POST'])
def process():

    text = request.form['input_text']

    if text:
        
        # compute text variables:
        

        diff_word_cnt = len(find_difficult_words(text))
        sentences = split_clean_sent(text.split('\n')) # list: all tokenized sentences
        sent_cnt = len(sentences) # int: amount of sentences in text

        words = tokenize_clean(sentences) # list: all tokenized words
        word_cnt = len(words) # int: amount of words in text
        syllable_cnt = count_syl(words) # int: amount of syllables in text
        par_cnt = count_par(text)
        char_cnt = count_char(text)
        word_per_par = word_cnt/par_cnt

        avg_sent_word = word_cnt/sent_cnt # float: average words per sentence
        avg_word_char = avg_char(words) # float: average characters per word
        avg_word_syll = syllable_cnt/word_cnt # float: average syllables per word

        # compute some readability scores

        brouwer_index = get_brouwerid(avg_word_syll,avg_sent_word)
        douma_score = get_douma(avg_word_syll, avg_sent_word)
        ari_score = get_ari(avg_word_char, avg_sent_word)
        # get text with html entities
        html_text = html_entities(text)
        
        # return results in json-format.
        return jsonify({'out' : text, 'html_text' : html_text,
                        'other' : '<tr><td>Karakters</td><td>'+str(char_cnt)+'</td></tr>'+
                                  '<tr><td>Woorden</td><td>'+str(word_cnt)+'</td></tr>'+
                                  '<tr><td>Zinnen</td><td>'+str(sent_cnt)+'</td></tr>'+
                                  '<tr><td>Paragrafen</td><td>'+str(par_cnt)+'</td></tr>'+
                                  '<tr></tr>'+
                                  '<tr><td>Zeldzame woorden</td><td>'+str(diff_word_cnt)+'</td></tr>'+
                                  '<tr><td>Zeldzame woorden per paragraaf</td><td>'+str(round((diff_word_cnt/par_cnt), 2))+'</td></tr>'+
                                  '<tr></tr>'+
                                  '<tr><td>Woorden per paragraaf gemiddeld</td><td>'+str(round(word_per_par, 2))+'</td></tr>'+
                                  '<tr><td>Woorden per zin gemiddeld</td><td>'+str(round(avg_sent_word, 2))+'</td></tr>'+
                                  '<tr><td>Karakters per woord gemiddeld</td><td>'+str(round(avg_word_char, 2))+'</td></tr>'+
                                  '<tr><td>Lettergrepen per woord gemiddeld</td><td>'+str(round(avg_word_syll, 2))+'</td></tr>'+
                                  '<tr></tr>'+
                                  '<tr><td>Brouwer Index</td><td>'+str(round(brouwer_index, 2))+'</td></tr>'+
                                  '<tr><td>Douma Score</td><td>'+str(round(douma_score, 2))+'</td></tr>'+
                                  '<tr><td>ARI Score</td><td>'+str(round(ari_score, 2))+'</td></tr>'+
                                  '<tr></tr>'+
                                  '<tr><td>Lees tijd</td><td>'+get_readtime(word_cnt)+'</td></tr>'+
                                  '<tr><td>Spreek tijd</td><td>'+get_speaktime(word_cnt)+'</td></tr>'})

    return jsonify({'error' : 'Please import a file'})


def html_entities(text):
    '''Converts special characters to html entities'''
    return text.replace('&', '&amp;').replace('<', '&#60;').replace('>', '&#62;').replace('"', '&quot;')


if __name__ == '__main__':
    app.run(debug=True)