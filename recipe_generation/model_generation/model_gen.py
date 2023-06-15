from transformers import AutoTokenizer, DataCollatorForSeq2Seq, AutoModelForSeq2SeqLM
from accelerate import Accelerator, DeepSpeedPlugin
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import load_dataset
import datasets
from model_bart import bart_model, tokenize

model_path = 'sn4kebyt3/ru-bart-large'
dataset_path = '../datasets/out.csv'
bart_token = tokenize(model_path, load_dataset("csv", data_files=dataset_path)['train'], ['input', 'label'])
tokenized_dataset = bart_token.make_tokenized_dataset()
model = bart_model(model_path, tokenized_dataset, 4)
model.train()