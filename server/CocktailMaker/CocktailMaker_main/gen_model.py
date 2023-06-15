from transformers import AutoTokenizer, DataCollatorForSeq2Seq, AutoModelForSeq2SeqLM
from accelerate import Accelerator, DeepSpeedPlugin
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import load_dataset

class bart_model:
    def __init__(self):
        model_path = '/home/outcast/PycharmProjects/project/hse_padii_2023_python_project_cocktail_maker/server/CocktailMaker/CocktailMaker_main/model2'
        tokenizer_path = '/home/outcast/PycharmProjects/project/hse_padii_2023_python_project_cocktail_maker/server/CocktailMaker/CocktailMaker_main/tokenizer2'
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.bart2bart = AutoModelForSeq2SeqLM.from_pretrained(model_path).to('cuda:0')

a = bart_model()