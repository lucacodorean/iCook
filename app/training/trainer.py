from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "distilgpt2"
device = "gpu"

model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

import pandas as pd

df = pd.read_csv("/content/drive/MyDrive/distilgpt2-training/dataset/RecipeNLG_dataset.csv")

from datasets import Dataset
import pandas as pd
import json

def map_dataset(batch):
  return tokenizer(
      batch["formatted_text"],
      truncation=True,
      max_length=128,
      return_overflowing_tokens=True,
  )

df = df[:20000]
def convert_to_text(row):
    title = row['title']
    ingredients = json.loads(row['ingredients'])  
    directions = row['directions']
    link = row['link']
    source = row['source']
    ner = json.loads(row['NER'])

    formatted_text = (
        f"Title: {title}\n"
        f"Ingredients: {', '.join(ingredients)}\n"
        f"Directions: {directions}\n"
        f"Link: {link}\n"
        f"Source: {source}\n"
        f"NER: {', '.join(ner)}"
    )
    return formatted_text

df['formatted_text'] = df.apply(convert_to_text, axis=1)

dataset = Dataset.from_pandas(df)
dataset = dataset.map(
    map_dataset,
    batched=True, 
    batch_size = 8, 
    remove_columns=list(df.columns)
)

dataset = dataset.remove_columns(["overflow_to_sample_mapping"])
dataset = dataset.train_test_split(train_size=0.8, test_size=0.2)

from transformers import DataCollatorForLanguageModeling

data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)
data_collator

from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="/content/drive/MyDrive/distilgpt2-training/results",
    evaluation_strategy="epoch",
    num_train_epochs=10,
    learning_rate=2e-5,
    weight_decay=0.01
) 

trainer = Trainer(
    model=model,
    train_dataset = dataset["train"],
    eval_dataset = dataset["test"],
    args=training_args,
    data_collator=data_collator
)

trainer.train()
tokenizer.save_pretrained(training_args.output_dir)