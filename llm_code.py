import json
import google.generativeai as genai


# load  configuration JSON 
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Accessing API key 
api_k = config.get('api_key')

genai.configure(api_key=api_k)

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

instruction ="""
Analyze the website description and determine if it should be accepted. The website must explicitly offer services to clients using actionable phrases like "We deliver," "We assist with," "We support," "Our expertise covers," "We help clients achieve," "We bring you," "We focus on," "We guide clients through," "We cater to," or "We aim to help." 
The services must clearly fall under categories like Web Design, Web Development, SEO Agency, Ads Agency, Digital Marketing Agency, Website Creation, SEO Services, Marketing Services, or similar. Respond "YES" if the website clearly offers these services to clients, using specific phrases. Respond "NO" if the website only discusses the industry or terms in general (e.g., "SEO is a strategy") or does not explicitly state they offer these services.followed by one line reason for your answer. If you are unable to determine, respond "UNKNOWN" and provide a reason.
"""

def llm_gemini_innit():
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Create the model
    generation_config = {
      "temperature": 0.4,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 200,
      "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=generation_config,
      system_instruction=instruction,
    )
    return model



def website_verdict(prompt, model):
    token_p = model.count_tokens(prompt).total_tokens
    if token_p < 2000:
        response = model.generate_content(prompt)
    return response
