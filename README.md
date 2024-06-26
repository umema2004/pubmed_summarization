# PubMed Article Summarization Web Application
### Umema Ashar | 22i-2036 | BS Data Science 

## Overview
This documentation provides a comprehensive guide to developing a web application that summarizes PubMed articles. The application employs Flask as the backend framework and includes functionalities for user authentication, text preprocessing, extractive summarization, and file saving. This guide covers data exploration, model selection (for summarization), fine-tuning (optional), and web application development.

### Breakdown of files
app.py: implementation of the web application

summarize.py: summarization performed on the PubMed Summarization dataset from HuggingFace

templates folder: html files for frontend

static folder: static items (images, etc)

file.txt: a sample file containing an article

using-genAI: folder containing app.py which is the application deployment and templates folder containing html files

## Setup Instructions
Clone repository:
git clone https://github.com/umema2004/pubmed_summarization

cd pubmed_summarization

cd summarizer-genai

## Install Dependencies:
pip install -r requirements.txt

## Run the Application:
python app.py

Login with the username and passwords from the users.csv file
Paste any article you would like to summarize OR select a text file containing an article and select length of summary
click 'Summarize'
click 'save' if you wish to save the save the summary in a text file
have fun

## Model Selection and Fine-tuning
### Extractive Summarization: 
Select sentences from the original text based on importance scores (e.g., word frequency, TF-IDF).
Implement extractive summarization using NLTK for tokenization, stopwords removal, and sentence scoring.

## Web Application Development
### Framework:
Flask is used for backend development due to its simplicity and flexibility in handling HTTP requests and responses.

### Functionality:
User Authentication: Implement login and logout functionalities using sessions and a simple CSV-based user database.
Text Preprocessing: Clean and preprocess input PubMed articles. expand contractions, convert to lower case, remove special characters, remove extra spaces, tokenize, remove stop words, lemmetization
Summarization: Implement extractive summarization based on word frequency or integrate generative models for abstractive summarization (optional).
File Handling: Allow users to input text directly or upload a file containing PubMed article data.
Output: Display both the original article and its summarized version on the web interface. Generate an image based on the text input and a bar graph visualizing quality metrics of the summary.
Optional Features (Advanced):
User Authentication: Manage user sessions securely with Flask sessions and ensure credentials are stored and verified.
Customization: Allow users to select the style or length of the summary (brief, detailed).
File Saving: Enable users to save the original article and its summary as text files for future reference.
Image generation (unsuccessful): I could not generate an image so you get 3 very cute cats.
Metrics evaluation: A bar graph is generated based on evaluation metrics of quality of summary (precision, recall, F1 score)

# Gen-AI:
## Usage
### Home Page (/):

Displays a simple input form where users can enter paragraphs of text to summarize.
### Summarize Endpoint (/summarize):

Handles POST requests to summarize the provided paragraph using the OpenAI GPT-3 model (text-davinci-003).
Returns the original paragraph and its summarized version to the user interface.
## Functionality
### Text Summarization:

Uses OpenAI GPT-3 to generate concise summaries of scientific text based on the provided paragraph.
Summaries are generated with a maximum of 100 tokens for brevity.
### User Interface:

Renders the input form and displays both the original paragraph and its summarized version after submission.

# author:

Umema Ashar | 22i-2036
