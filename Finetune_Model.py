# 导入必要的库
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

# 导入模型
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,  # 启用 4-bit 量化
    bnb_4bit_compute_dtype=torch.float16,  # 使用 float16 计算
    bnb_4bit_use_double_quant=True,  # 启用双量化（减少显存）
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config,  # 4-bit 量化配置
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)

print(model)

dataset = load_dataset("json", data_files="data.json")["train"]


def convert_to_conversation(sample):
    return {
        "messages": [
            {"role": "user", "content": sample["content"]},
            {"role": "assistant", "content": sample["response"]},
        ]
    }


train_data = dataset.map(convert_to_conversation)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_data,
    args=SFTConfig(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        max_steps=100,
        learning_rate=1e-4,
        fp16=True,
        optim="adamw_8bit",
        max_seq_length=1024,
        remove_unused_columns=False,
    ),
)

trainer.train()

model.save_pretrained("finetuned_model")
tokenizer.save_pretrained("finetuned_model")
