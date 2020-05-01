import flask
from flask import Flask, render_template , url_for , request
from flask_bootstrap import Bootstrap
from flask_assets import Bundle, Environment
from flask import render_template, Flask, request, flash
# from luhn_summarizer import luhn_summarizer

app = Flask(__name__)
type_of_summaries = ['luhn']

js = Bundle('sam.js','jquery.min.js','jquery-migrate-3.0.1.min.js','popper.min.js','bootstrap.min.js','jquery.easing.1.3.js','jquery.waypoints.min.js','jquery.stellar.min.js','owl.carousel.min.js','jquery.magnific-popup.min.js','aos.js','jquery.animateNumber.min.js','bootstrap-datepicker.js','jquery.timepicker.min.js','particles.min.js','particle.js','scrollax.min.js','google-map.js','main.js', output = 'gen/main.js')
css = Bundle ('icomoon.css','style.css','flaticon.css','jquery.timepicker.css','magnific-popup.css','aos.css','owl.theme.default.min.css','owl.carousel.min.css','animate.css',output ='gen/main.css')
assets = Environment(app)

assets.register('main_js',js)
assets.register('main_css',css)

@app.route("/")
def home():
    return render_template("home.html")

# @app.route("/about")
# def home():
#     return "<h1>Hello newyork!</h1>"

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    # print('summar')
    if request.method == 'POST':
        text = request.form['text']
        num_sent = None
        if request.form['num_sentences']:
            num_sent = request.form['num_sentences']

        type_of_summary = request.form['type_of_summ']
        if type_of_summary == 'luhn':
            summary = luhn_summarize(text, num_sent=num_sent)
            return render_template("home.html", summary=summary)

        # elif type_of_summary == 'textrank':
        #     summary = textrank_summarize(text, num_sent=num_sent)
        #     return render_template("index.html", summary=summary)
    else:
    	return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)

import re
import nltk
from nltk import sent_tokenize, word_tokenize
from collections import Counter
import sentencepiece as spm
kannada_sample_text = "ಬೆಂಗಳೂರಿನಲ್ಲಿ ಆಫ್ರಿಕಾ ಮಹಿಳೆಯರ ವೇಶ್ಯಾವಾಟಿಕೆ ದಂಧೆ; ಪೊಲೀಸರ ಮುಂದೇ ಅರೆ ನಗ್ನಳಾಗಿ ಕೂಗಾಡಿದ ಮಹಿಳೆ"
with open("stop_words.txt",encoding='utf-8') as f:
    d=(f.read()).strip('\n')

stopwords=d.split('\n')

def tokenize(text):        
        sp = spm.SentencePieceProcessor()
        sp.Load("C:/Users/samruddhi/Documents/computing/kannada_lm.model")
        return sp.EncodeAsPieces(kannada_sample_text)

class Luhn_Summarizer():
    def __init__(self):
        pass
    

    def clean_and_tokenize(self, article_text):
        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        #sentence tokenization
        sentences = nltk.sent_tokenize(article_text)
        print(sentences)

        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        return sentences, formatted_article_text


    def find_word_frequencies(self, cleaned_text):
#         print(tokenize(cleaned_text))
        word_frequencies = Counter(tokenize(cleaned_text))
#         print(word_frequencies)
        
#         for word in nltk.word_tokenize(cleaned_text):
#             if word not in stopwords:
#                 if word not in word_frequencies.keys():
#                     word_frequencies[word] = 1
#                 else:
#                     word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

        return word_frequencies

    def calculate_sentence_scores(self, sentences, word_frequencies):
        sentence_scores = {}
        for sent in sentences:
#             for word in nltk.word_tokenize(sent.lower()):
            for word in tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        return sentence_scores

    def summarize(self, article, num_sent=None):
        sentences, cleaned_text = self.clean_and_tokenize(article)
        original_length = len(sentences)
        word_freq = self.find_word_frequencies(cleaned_text)
        sentence_scores = sorted(self.calculate_sentence_scores(sentences, word_freq), reverse=True)
        if num_sent:
            if int(num_sent) < original_length:
                return ' '.join(sentence_scores[:int(num_sent)])
        if original_length > 5:
            return ' '.join(sentence_scores[:5])
        else:
            return 'Too short to summarize'

def luhn_summarize(text, num_sent=None):
    summarizer = Luhn_Summarizer()
    summary = summarizer.summarize(text, num_sent=num_sent)
    return summary

with open("stop_words.txt",encoding='utf-8') as f:
    d=(f.read()).strip('\n')

stopwords=d.split('\n')
print(stopwords)

