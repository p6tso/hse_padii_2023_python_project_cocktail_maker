from transformers import AutoTokenizer, DataCollatorForSeq2Seq, AutoModelForSeq2SeqLM
from accelerate import Accelerator, DeepSpeedPlugin
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import load_dataset
import datasets

max_input_length = 50
max_target_length = 300
class bart_model:
    def __init__(self, model_name, dataset_path, batch_size):
        self.model_name = model_name
        self.dataset_path = dataset_path
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.bart2bart = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to('cuda:0')
        self.max_input_length = 50
        self.max_target_length = 300
        self.tokenized_datasets = self.make_tokenized_dataset()
        self.args = self.make_model_args()
        self.batch_size = batch_size
        self.rouge = datasets.load_metric("rouge")
        self.data_collator = DataCollatorForSeq2Seq(self.tokenizer, model=self.bart2bart)
        self.trainer = self.make_trainer()
    def make_trainer(self):
        trainer = Seq2SeqTrainer(
            self.bart2bart,
            self.args,
            train_dataset=self.tokenized_datasets,
            eval_dataset=self.tokenized_datasets,
            data_collator=self.data_collator,
            tokenizer=self.tokenizer,
            compute_metrics=self.compute_metrics
        )
        return trainer
    def make_model_args(self):
        args = Seq2SeqTrainingArguments(
            output_dir='./drive/MyDrive/checkpoints',
            evaluation_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            weight_decay=0.01,
            save_total_limit=3,
            num_train_epochs=1,
            prediction_loss_only=True,
            logging_steps=2,
            predict_with_generate=True,
            fp16=True,
            push_to_hub=True,
        )
        return args
    def make_tokenized_dataset(self):
        dataset = load_dataset("csv", data_files="dataset_for_generation.csv")['train']
        tokenized_datasets = dataset.map(self.preprocess_function, batched=True, batch_size=4,
                                         remove_columns=["label", "input", "name"])
        return tokenized_datasets
    def preprocess_function(self, examples):
        try:
            model_inputs = self.tokenizer(examples['input'], max_length=self.max_input_length, truncation=True, add_special_tokens=True, padding = True).copy()
            labels = self.tokenizer(examples['label'], max_length=self.max_target_length, truncation=True, add_special_tokens=True, padding = True)
            model_inputs["labels"] = labels["input_ids"].copy()
        except:
            model_inputs = self.tokenizer(['', '', '', ''], max_length=self.max_input_length, truncation=True, add_special_tokens=True, padding = True).copy()
            labels = self.tokenizer(['', '', '', ''], max_length=self.max_target_length, truncation=True, add_special_tokens=True, padding = True)
            model_inputs["labels"] = labels["input_ids"].copy()
        return model_inputs

    def compute_metrics(self, pred):
        labels_ids = pred.label_ids
        pred_ids = pred.predictions
        pred_str = self.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
        labels_ids[labels_ids == 1] = self.tokenizer.pad_token_id
        label_str = self.tokenizer.batch_decode(labels_ids, skip_special_tokens=True)
        rouge_output = self.rouge.compute(predictions=pred_str, references=label_str, rouge_types=["rouge2"])["rouge2"].mid
        return {
            "rouge2_precision": round(rouge_output.precision, 4),
            "rouge2_recall": round(rouge_output.recall, 4),
            "rouge2_fmeasure": round(rouge_output.fmeasure, 4),
        }
    def train(self):
        self.trainer.train()


model = bart_model('sn4kebyt3/ru-bart-large', '../datasets/dataset_for_generation.csv', 4)
model.train()