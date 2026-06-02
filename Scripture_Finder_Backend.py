import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests
import json

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

YV_KEY = os.environ.get("YV_KEY")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY") 

@app.route('/')
def index():
    return app.send_static_file('bible_reader.html')

@app.route('/api/verses')
def verses():
    version = request.args.get('version', '111')
    book = request.args.get('book', 'JHN')
    chapter = request.args.get('chapter', '1')
    passage_id = f"{book}.{chapter}"
    url = f"https://api.youversion.com/v1/bibles/{version}/passages/{passage_id}"
    res = requests.get(url, headers={"X-YVP-App-Key": YV_KEY})
    return res.json(), res.status_code

@app.route('/api/recommend', methods=['POST'])
def recommend():
    situation = request.json.get('situation', '')

    headers = {

    'Authorization': f'Bearer {OPENROUTER_KEY}',

    'HTTP-Referer': '<YOUR_SITE_URL>',

    'X-OpenRouter-Title': '<YOUR_SITE_NAME>',

    'Content-Type': 'application/json',

    }

    response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json={

    'model': 'meta-llama/llama-3.3-70b-instruct',

    'messages': [{ 'role': 'user', 'content': f"""Someone has described their situation: "{situation}"

            Recommend exactly one Bible chapter that would comfort or help them.
            Reply with ONLY a JSON object in this format, nothing else:
            {{"book": "JHN", "chapter": 3, "language": "the language the situation is written in" "summary": "write roughly ten sentences explaining the chapter and how it may help in the language of the described situation"}}

            Use standard USFM book codes (GEN, EXO, PHP, PRO, ISA, MAT, MRK, LUK, JHN, ROM, PSA, etc.). Philippians is PHP, not PHI"""}],

    'provider': {

        'sort': 'throughput',

    },

    })

    data = response.json() # convert to python dict

    print("===RESPONSE===")
    print(data['choices'][0]['message']['content'])
    print()

    return json.loads(data['choices'][0]['message']['content']) # returns the LLM's response as a JSON object

if __name__ == '__main__':
    app.run(port=5000)
