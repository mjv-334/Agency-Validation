from playwright.sync_api import sync_playwright
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import csv 
import re
import tiktoken

# Choose the model's tokenizer (e.g., 'gpt-3.5-turbo' or 'gpt-4') get token number

encoder = tiktoken.get_encoding("cl100k_base")

#stopwords dataset
stop_words = set(stopwords.words('english'))

def words_tokenize(final_lst):
  joined_string = " ".join(final_lst)
  
  token_p = encoder.encode(joined_string) # get number of tokens based on openai tokenizer
  print("before filteration: ",len(token_p)) # original token number 

  words = word_tokenize(joined_string) #nltk tokenizer

  filtered_words = [word for word in words if word.lower() not in stop_words and word.isalpha()] #nltk remove stopwords
  filtered_text = " ".join(filtered_words) #make list into a string
  
  token_p = encoder.encode(filtered_text) 
  print("after filteration: ",len(token_p)) # preprocessed string token number

  # just write the origginal string and preprocessed string for dev purpose
  with open("Original.txt", "w",  encoding='utf-8') as file:
    file.write(joined_string)

  with open("filtered.txt", "w",  encoding='utf-8') as file:
    file.write(filtered_text)

  return filtered_text


def get_web_text(file_url): 
  # accepts url gives out final_list containing all div,h and p texts
  p_lst = []
  h_lst = []
  div_lst = []

  #browser
  with sync_playwright() as p:
    # Launch headless Chromium browser
    browser = p.chromium.launch(headless=True)# headless=True runs in background
    page = browser.new_page()

    # Navigate to the url
    try:
      page.goto(file_url)
    
    except:
      return False
      # Wait for the page to load completely
    page.wait_for_load_state('load')# wait for page to be in 'load' state

    #get content

    tok = 0 # token count
    elem = 0 # distinct element count

    # get all headings
    headings_all = page.query_selector_all('h1, h2, h3, h4')
    for heading in headings_all:
      h_lst.append(heading.inner_text())

    tok = 0 # token count
    elem = 0 # distinct element count

    # Select all <div> elements
    div_elements = page.query_selector_all('div')
    for div in div_elements:
    # text content div
      text = div.inner_text().strip()
      tok += len(encoder.encode(text)) #count token to ensure it doesnt go over limit
      if tok >=1000 or elem > 20:
        break
      
      if text: # Only add divs that contain text 
        div_lst.append(text)
        elem += 1


    tok = 0 # token count
    elem = 0 # distinct element count
    
    # Select all p elements on the page
    p_elements = page.query_selector_all('p')  
    for element in p_elements:
      text = element.inner_text()
      tok += len(encoder.encode(text))
      if tok >=1000 or elem > 30:
        break
      
      p_lst.append(text)
      elem += 1

    #close browser
    page.context.clear_cookies()
    browser.close()
    return div_lst + h_lst + p_lst


def store_verdict(verdict_string, user_input):
  words = verdict_string.split()
  verdict = ""
  if re.match(r'^yes', verdict_string, re.IGNORECASE):
    verdict = "Accepted"
  elif re.match(r'^no', verdict_string, re.IGNORECASE):
    verdict = "Denied"
  else:
    verdict = "INVALID"

  verdict_string = " ".join(words[1:]) 

  row_data = [user_input["name"], user_input["url"], user_input["email"],  verdict, verdict_string]
  with open("results.csv", mode='a', newline='', encoding='utf-8') as csvfile:
      csvwriter = csv.writer(csvfile)

      # Write the row to the file
      csvwriter.writerow(row_data)
  return row_data
