# pip install transformers           

import torch                

from transformers, import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained('t5-base')                        
model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

inputs = tokenizer.encode("summarize: " + text, return_tensors='pt', max_length=512, truncation=True)          

summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2)         

summary = tokenizer.decode(summary_ids[0])