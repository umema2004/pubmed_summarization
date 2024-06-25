from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = 'shhhhh'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    paragraph = request.form['paragraph']
    summary = generate_summary(paragraph)
    return render_template('index.html', summary=summary, paragraph=paragraph)

def generate_summary(paragraph):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize the following paragraph:\n\n{paragraph}",
        max_tokens=100
    )
    summary = response.choices[0].text.strip()
    return summary

if __name__ == '__main__':
    app.run(debug=True)
