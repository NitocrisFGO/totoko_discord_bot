# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import re

device = "cuda"
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")

prompt = "你好，你是谁？"

messages = [{"role": "user", "content": prompt}]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
model_inputs = tokenizer(
    text=[text],
    padding=True,
    return_tensors="pt",)
model_inputs = model_inputs.to("cuda")

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
