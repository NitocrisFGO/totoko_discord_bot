from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

# load JSON file as Hugging Face Dataset
dataset = load_dataset("json", data_files="data.json")

device = "cuda"
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
                                             device_map="auto",
                                             offload_folder="./offload",)
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")

# function for data pre-process
def preprocess_data(examples):
    inputs = [f"<|User|>{inp}<|Assistant|>" for inp in examples["content"]]
    outputs = examples["response"]
    model_inputs = tokenizer(
        inputs,
        max_length=512,
        truncation=True,
        padding="max_length",
    )
    # set labels，what need to be generated
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            outputs,
            max_length=512,
            truncation=True,
            padding="max_length",
        )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


# print info for dataset
tokenized_dataset = dataset["train"].map(preprocess_data, batched=True)
print(tokenized_dataset[0])

# training parameters
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="no",
    save_strategy="steps",
    logging_dir="./logs",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=5e-5,
    fp16=True,
)

# create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
)

# start training
trainer.train()

# save model
model.save_pretrained("./finetuned_model")
tokenizer.save_pretrained("./finetuned_model")