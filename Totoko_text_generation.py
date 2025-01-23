# Load model directly
from transformers import AutoModelForCausalLM, AutoTokenizer
import re

device = "cuda"

tokenizer = AutoTokenizer.from_pretrained("kxdw2580/Qwen2.5-3B-Instruct-Uncensored-Test")
model = AutoModelForCausalLM.from_pretrained("kxdw2580/Qwen2.5-3B-Instruct-Uncensored-Test")

model = model.to(device)


prompt = "你知道什么叫，做爱吗？"

messages = [{"role": "user", "content": prompt}]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

model_inputs = tokenizer(
    text=[text],
    max_length=512,
    truncation=True,
    padding="max_length",
    return_tensors="pt"
).to(device)

# Generate response with optimized parameters
generated_ids = model.generate(**model_inputs, max_new_tokens=512)
generated_ids_trimmed = [
    out_ids[len(in_ids):] for in_ids, out_ids in zip(model_inputs.input_ids, generated_ids)
]

# Decode generated tokens to text
output_text = tokenizer.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)

cleaned_text = [re.sub(r"<.*?>", "", text).strip() for text in output_text]

print(cleaned_text[0])
