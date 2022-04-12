# The Bugs - NTB text assessor 
##### Nederlandse Tekst Beoordeler


## Authors:
- Gerjon Schuurman (GSrman): flask, interface
- David Poot (DBPoot): readability, textdata
- Martine Elzinga (e10tien): word difficulty, text mistakes

Everyone helped eachother with bugfixing and connecting the programs.


## Description:
Our program lets a user upload a text file on a web interface. We created this interface using flask to clearly and sufficiently give the data to the user. From this text we calculate several readability scores to declare whether the text is easy to read and what level education it is considered. It also gives general data, like word count, paragraph count etc. 
Our program is specifically designed for the dutch language.


## Technologies/Requirements
- [nltk](https://www.nltk.org/)
- [wordfreq](https://github.com/rspeer/wordfreq)
- [flask](https://flask.palletsprojects.com/)

## Setup

```
$ cd TheBugs
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install Flask
$ pip install nltk
$ python3
>>> import nltk
>>> nltk.download("punkt")
>>> exit()
$ pip3 install wordfreq
$ deactivate
```

## Usage

```
$ . venv/bin/activate
$ . export FLASK_APP=process
$ flask run
```

Open the given http://something (by default http://127.0.0.1:5000/) in a browser.
Then you can upload a .txt file, which it will process and
do some calculations.