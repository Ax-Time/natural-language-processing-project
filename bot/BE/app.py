from flask import Flask
from flask import request
from flask import jsonify
import yaml
from typing import Dict
from flask_cors import CORS, cross_origin
import numpy as np
import wikipediaapi

import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# this model is a zero-shot / few-shot model, general purpose, trained on a large corpus of text
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", device_map="auto", torch_dtype=torch.float32)


wiki_wiki = wikipediaapi.Wikipedia('en')

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)


class DataStore():
   wikipedia: None

data = DataStore()

@app.route('/', methods=['POST'])
def index():
    # context = request.json['context']
    question = request.json['question']

    print("context of wikipedia", data.wikipedia)

    # context = wiki_wiki.page(context).summary
    
    input_text = f'Try to give some ideas about <Knowledge-base> {data.wikipedia} </knowledge-base> Question : {question}'

    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)

    output_ids = model.generate(input_ids, max_new_tokens=1000, pad_token_id=tokenizer.eos_token_id)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Access-Control-Allow-Methods']='GET, POST, PUT, OPTIONS'
    response.headers["Access-Control-Allow-Headers"]="Access-Control-Request-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Headers,Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept"
    return output_text

@app.route('/context', methods=['POST'])
def context():
    context = request.json['context']
    data.wikipedia = wiki_wiki.page(context).summary

    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Access-Control-Allow-Methods']='GET, POST, PUT, OPTIONS'
    response.headers["Access-Control-Allow-Headers"]="Access-Control-Request-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Headers,Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept"
    return "Selected Context: " + context

# import whisper

# # use fp32 for faster inference
# whisper_model = whisper.load_model("base.en")

# @app.route('/audio', methods=['POST'])
# def audio():
#     # get audio data from request
#     file = request.files['audio_file']

#     # file.save("audio.wav")
#     # result = whisper_model.transcribe("audio.wav", fp16=False, language="pt")

#     result = whisper_model.transcribe(file, fp16=False, language="pt")

#     response = jsonify({'some': 'data'})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers['Access-Control-Allow-Origin']='*'
#     response.headers['Access-Control-Allow-Methods']='GET, POST, PUT, OPTIONS'
#     response.headers["Access-Control-Allow-Headers"]="Access-Control-Request-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Headers,Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept"


#     # answering

#     question = result['text']
#     print(question)
#     parlai_agent.observe({'text': question})
#     passages = parlai_agent.act()
#     text = passages['text_candidates'][0]

#     input_text = f"Given the following passage, answer the related question in creative way.\n\nPassage:\n{passages['text_candidates'][0][:511]}\nQ: {question}?"
#     input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)

#     output_ids = model.generate(input_ids, max_new_tokens=32, pad_token_id=tokenizer.eos_token_id)
#     output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

#     response = jsonify({'some': 'data'})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers['Access-Control-Allow-Origin']='*'
#     response.headers['Access-Control-Allow-Methods']='GET, POST, PUT, OPTIONS'
#     response.headers["Access-Control-Allow-Headers"]="Access-Control-Request-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Headers,Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept"
#     return {'output': output_text, 'given': question}

if __name__ == "__main__":
    app.run(debug=True)