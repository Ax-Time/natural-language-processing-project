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
   input: None

data = DataStore()

data.input = ""

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




from transformers import GPTNeoForCausalLM, AutoTokenizer

model_id = "EleutherAI/gpt-neo-125M"
fine_tuned_id = "gidonofrio/gpt-neo-125M-finetuned"

default_device = 'cpu'
device = torch.device('cuda' if torch.cuda.is_available() else default_device)

tokenizer = AutoTokenizer.from_pretrained(model_id, padding_side='left')
model = GPTNeoForCausalLM.from_pretrained(fine_tuned_id, torch_dtype=torch.float32).to(device)

from parlai.core.agents import create_agent
from parlai.agents.image_seq2seq.image_seq2seq import ImageSeq2seqAgent
from parlai.scripts.interactive import setup_args


# using my local file path
local_file_path = 'zoo:wizard_of_wikipedia/knowledge_retriever/model'
parlai_agent_kwargs = {"model_file": local_file_path}

parser = setup_args()
opt = parser.parse_kwargs(**parlai_agent_kwargs)
parlai_agent = create_agent(opt, requireModelExists=True)

@app.route('/reset', methods=["POST"])
def reset():
    data.input = ""
    data.wikipedia = ""

    return "Ok"

@app.route('/gpt-question', methods=['POST'])
def gpt_question():
    text = request.json['text']
    context = request.json['context']
    persona = request.json['persona']
    turn = request.json['turn']

    parlai_agent.observe({'text': text, 'episode_done': True})
    output = parlai_agent.act()
    passage = output['text']

    # CHOSEN_TOPIC
    # PERSONA
    # SPEAKER
    # PASSAGE -> CONTEXT
    # TEXT -> QUESTION

# fix france
    # input_text = f"""
    #     CHOSEN_TOPIC: Pharmacist
    #     PERSONA: I am a pharmacist
    #     SPEAKER: 0_Apprentice
    #     TEXT: {text}

    #     SPEAKER: 1_Wizard
    #     PASSAGE: {passage}
    #     TEXT:"""


    if (turn == 1):
        input_text = f"""CHOSEN_TOPIC: {context}\nPERSONA: {persona}\nSPEAKER: 0_Wizard\nPASSAGE: {passage}\nTEXT: {text}\n\nSPEAKER: 1_Apprentice\nTEXT:"""
    else:
        input_text = f"""SPEAKER: 0_Wizard\nPASSAGE: {passage}\nTEXT: {text}\n\nSPEAKER: 1_Apprentice\nTEXT:"""
    data.input = data.input + input_text

    tokenizer.pad_token = tokenizer.eos_token

    gpt_input = tokenizer.encode(data.input, return_tensors='pt').to(device)
    output_len = len(data.input) + 100
    output = model.generate(gpt_input, pad_token_id=tokenizer.eos_token_id, do_sample=True, max_length=output_len, top_p=0.95, top_k=60)

    output = tokenizer.decode(output[0], skip_special_tokens=True)


    splitted_output = output.split('\n')

    filtered_output = ""

    k = 0
    for i in range(len(splitted_output)):
        if splitted_output[i].lstrip().startswith('SPEAKER: 1_Apprentice'):
            k += 1
            if(k == turn):
                filtered_output = splitted_output[i+1].lstrip()
                break

    data.input = data.input + filtered_output[5:] + "\n\n"

    print(data.input)

    return filtered_output[5:]
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