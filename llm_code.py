import json
import google.generativeai as genai


# load  configuration JSON 
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Accessing API key 
api_k = config.get('api_key')

genai.configure(api_key=api_k)

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

instruction ="""Analyze the website description provided and determine if it mentions explicitly or implicitly they offers services to clients. The services in  should be related to areas like service agency, Web Design, Web Development, SEO Agency, Ads Agency, Digital Marketing Agency, Website Creation, SEO Services, Marketing Services, or similar.

Look for actionable language that directly communicates service provision, such as:
  Delivering solutions,Offering expertise, Helping clients with, Assisting to develop,Creating strategies,Empowering businesses,Building solutions,
Crafting solutions, We deliver,We assist with,We help clients achieve,We guide clients through,Our expertise covers

Respond 'YES' ,'NO' or 'UNKNOWN' and sentence of less than 15 words with reason why 
    'YES' if the website clearly states or implies that they are offering services to clients, using actionable phrases or by describing specific service offerings
    'NO' if the website only discusses the general industry, expertise, or tools but does not provide any actionable phrase or clear indication that services are being offered.
    'UNKNOWN' if the website description is ambiguous or doesn't clearly indicate that services are being offered.That is you are not sure if they offer service or not. 
Please consider both the phrasing and the context of the website description when making your decision."""
def llm_gemini_innit():
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Create the model
    generation_config = {
      "temperature": 0.5,
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
