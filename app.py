from flask import Flask, request, render_template, redirect
import requests
import validators

import webscrape 
import llm_code
import mail_code

app = Flask(__name__)

user_input = {}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods = ['POST'])
def submit():
    url = request.form.get('url')
    email = request.form.get('email')
    name = request.form.get('name')
    #validate url
    if not validators.url(url):
        err_message = "Invalid URL"
        print(err_message)
        return render_template('error.html',message = err_message)
    #validate email
    if not validators.email(email):
        err_message = "email invalid"
        print(err_message)
        return render_template('error.html',message = err_message)
    user_input["name"] = name
    user_input["url"] = url
    user_input["email"] = email
    
    return redirect('/thank_you')

@app.route('/thank_you')
def thank_you():
    #scrape website and display verdict
    final_lst = webscrape.get_web_text(user_input["url"])
    if final_lst == False:
        return render_template('error.html',message = "invalid url")
    prompt = webscrape.words_tokenize(final_lst)
    print("Successfully scraped")
    model = llm_code.llm_gemini_innit()
    response = llm_code.website_verdict(prompt, model)
    print("Gemini response recieved")
    verdict_string = response.text
    print(verdict_string)
    row_data = webscrape.store_verdict(verdict_string, user_input) #name, url, email, verdict, reason
    print("Written to csv")
    print(row_data)
    if (not mail_code.send_mail(row_data)):
        return render_template('error.html',message = "Error in sending mail")
    return render_template('thanks.html')

def is_url_reachable(url):
    try:
        response = requests.get(url)
        return response.status_code == 200  # URL must be reachable (status 200)
    
    except requests.RequestException:
        return False

if __name__ == '__main__':
    app.run() 

