from flask import Flask, request, render_template, redirect, url_for, session
import csv
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
import string
import re
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
import time
import contractions

import nltk
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.secret_key = 'verysecretkey'  

# Directory for static files
static_dir = os.path.join(app.root_path, 'static')
os.makedirs(static_dir, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt'}

def generate_image_from_text(text):
    image_size = (400, 300)  
    image = np.ones(shape=(image_size[1], image_size[0], 3), dtype=np.uint8) * 255
    image = Image.fromarray(image)
    image_path = os.path.join(static_dir, 'generated_image.jpg')  
    image.save(image_path)
    return url_for('static', filename='image.jpg')

def create_metrics_bar_graph(metrics, labels, filename='metrics_bar.png'):
    y_pos = np.arange(len(labels))
    plt.figure(figsize=(10, 5))
    plt.bar(y_pos, metrics, align='center', alpha=0.5, color='b')
    plt.xticks(y_pos, labels)
    plt.ylabel('Score')
    plt.title('Summary Quality Metrics')
    plt.savefig(os.path.join(static_dir, filename))
    plt.close()
    return url_for('static', filename=filename)

def preprocess(text):
    text = contractions.fix(text)   
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    tokens = [word for word in tokens if word not in stop_words and not re.search(r'\d', word)]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    return tokens

def extractive_summarization(article, summary_style='brief'):
    sentences = sent_tokenize(article)
    words = preprocess(article)
    word_freq = Counter(words)
    sentence_scores = {sent: sum(word_freq[word] for word in preprocess(sent)) for sent in sentences}
    top_n = 3 if summary_style == 'brief' else 5
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:top_n]
    return ' '.join(summary_sentences)

def verify_credentials(username, password):
    with open('users.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_credentials(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials!")
    return render_template('login.html')

@app.route('/logout')
def logout(): 
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        summary_style = request.form.get('summary_style', 'brief')
        article = None
        
        if 'article' in request.form and request.form['article'].strip():
            article = request.form['article']
        elif 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                article = file.read().decode('utf-8')
            else:
                return render_template('index.html', error="Invalid file or file type!")
        
        if article:
            summary = extractive_summarization(article, summary_style)
            generated_image = generate_image_from_text(article)
            metrics = [0.85, 0.75, 0.65]  # Example metrics, normally calculated dynamically
            labels = ['Precision', 'Recall', 'F1-Score']
            graph_url = create_metrics_bar_graph(metrics, labels)
            return render_template('index.html', original_text=article, summary_text=summary, summary_style=summary_style, generated_image=generated_image, graph_url=graph_url)
        else:
            return render_template('index.html', error="No article provided!")
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_summary():
    original_text = request.form['original_text']
    summary_text = request.form['summary_text']
    filename = f"summary_{int(time.time())}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("Original Article:\n" + original_text + "\n\n")
        file.write("Summary:\n" + summary_text + "\n")
    return render_template('index.html', message="File saved successfully!", original_text=original_text, summary_text=summary_text)

if __name__ == '__main__':
    app.run(debug=True)
