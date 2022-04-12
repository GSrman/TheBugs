# File: process.py
# Author: G.J.H. Schuurman, David B. Poot
# Date: 12/04/2022
# The core: uses flask to render the webpage, and receives data to process,
# which it sents to and receives from the different required functions,
# and finally sends the required results back to the js file in json format.

from flask import Flask, render_template, request, jsonify
from readability import *
from timing import *
from word_difficulty import *
from sent_length import *
from spanify import add_span

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
        syllable_cnt, long_words_syll = count_syl(words) # int: amount of syllables in text
        par_cnt = count_par(text) # int: amount of paragraphs
        char_cnt = count_char(text) # int: amount of characters
        word_per_par = word_cnt/par_cnt # float: average amount of words per paragraph

        avg_sent_word = word_cnt/sent_cnt  # float: average words per sentence
        chars_cnt, avg_word_char, long_words_char = count_chars(words)  # float: average characters per word
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

        # compute some readability scores
        # Leesindex R.H.M. Brouwer (1963)
        brouwer_index = get_brouwerid(avg_word_syll, avg_sent_word)
        # AnalyseVanIndividualiseringsvormen reading level
        avi_level = get_avi(brouwer_index, avg_word_syll)
        # Dutch adjusted Flesch score
        douma_score = get_douma(avg_word_syll, avg_sent_word)
        # Education level associated with Douma score
        edu_level = get_edu(douma_score)
        # CEFR Reading level
        reading_level = get_readlevel(avg_sent_word)
        # Automated Readability Index
        ari_score = get_ari(avg_word_char, avg_sent_word)
        
        # get text with html entities
        html_text = html_entities(text)

        # mark difficult words in text
        diff_text = diff_words_html(html_text)

        # mark mistakes in text
        mistake_text = mistake_check_html(diff_text)
        
        # return results in json-format.
        return jsonify({'out' : text, 'html_text' : mistake_text,
                        'other' : '<tr><th>Algemene Informatie</th></tr>'+
                                  '<tr><td>Karakters</td><td>'+str(char_cnt)+'</td></tr>'+
                                  '<tr><td>Woorden</td><td>'+str(word_cnt)+'</td></tr>'+
                                  '<tr><td>Zinnen</td><td>'+str(sent_cnt)+'</td></tr>'+
                                  '<tr><td>Paragrafen</td><td>'+str(par_cnt)+'</td></tr>'+
                                  '<tr><th>Zeldzaam Woordgebruik</th></tr>'+
                                  '<tr><td>Zeldzame woorden</td><td>'+str(diff_word_cnt)+'</td></tr>'+
                                  '<tr><td title="~4 is het best">Zeldzame woorden per paragraaf</td><td>'+str(add_span("par_rare_word", round((diff_word_cnt/par_cnt), 1)))+'</td></tr>'+
                                  '<tr><th>Text Dichtheid</th></tr>'+
                                  '<tr><td title="~48-50 is het best">Woorden per paragraaf gemiddeld</td><td>'+add_span("par_words", round(word_per_par, 1))+'</td></tr>'+
                                  '<tr><td title="~15-20 is het best">Woorden per zin gemiddeld</td><td>'+str(round(avg_sent_word, 1))+'</td></tr>'+
                                  '<tr><td title="~11.5 is het best">Karakters per woord gemiddeld</td><td>'+add_span("word_char", round(avg_word_char, 1))+'</td></tr>'+
                                  '<tr><td title="<=3 is het best">Lettergrepen per woord gemiddeld</td><td>'+add_span("word_syll", round(avg_word_syll, 1))+'</td></tr>'+
                                  '<tr><th>Te Lange Woorden/Zinnen</th></tr>'+
                                  '<tr><td>Erg lange zinnen(Lettergrepen>30)</td><td>'+str(extra_long_sent_cnt)+" ("+str(extra_long_sent_pct)+'%)</td></tr>'+
                                  '<tr><td>lange zinnen(Lettergrepen>20)</td><td>'+str(long_sent_cnt)+" ("+str(long_sent_pct)+'%)</td></tr>'+
                                  '<tr><td>Lange Woorden(Lettergrepen>4)</td><td>'+str(long_words_syll_cnt)+" ("+str(long_words_syll_pct)+'%)</td></tr>'+
                                  '<tr><td>Lange Woorden(Karakters>12)</td><td>'+str(long_words_char_cnt)+" ("+str(long_words_char_pct)+'%)</td></tr>'+
                                  '<tr><th>Leesbaarheid</th></tr>'+
                                  '<tr><td title="0-120, lager is moeilijker">Brouwer Index</td><td>'+str(round(brouwer_index, 1))+'</td></tr>'+
                                  '<tr><td>AVI Niveau</td><td>'+str(avi_level)+'</td></tr>'+
                                  '<tr><td title="0-100, lager is moeilijker>Douma Score</td><td>'+str(round(douma_score, 1))+'</td></tr>'+
                                  '<tr><td>Opleidingsniveau</td><td>'+edu_level+'</td></tr>'+
                                  '<tr><td>CEFR Leesniveau</td><td>'+reading_level+'</td></tr>'+
                                  '<tr><td>ARI Score</td><td>'+str(round(ari_score, 1))+'</td></tr>'+
                                  '<tr><th>Duratie</th></tr>'+
                                  '<tr><td>Lees tijd</td><td>'+get_readtime(word_cnt)+'</td></tr>'+
                                  '<tr><td>Spreek tijd</td><td>'+get_speaktime(word_cnt)+'</td></tr>'})

    return jsonify({'error' : 'Please import a file'})


def html_entities(text):
    '''Converts special characters to html entities'''
    return text.replace('&', '&amp;').replace('<', '&#60;').replace('>', '&#62;').replace('"', '&quot;')


if __name__ == '__main__':
    app.run(debug=True)