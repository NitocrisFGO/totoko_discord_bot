from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-7B-Instruct-1M"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def generate(prompt):
    messages = [
        {"role": "system", "content": "以莱昂纳多·达·芬奇的角色性格和说话风格回答。"},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


state = 0

save_path = "./qwen2.5-7b-instruct"


model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

while state == 0:
    print("开始输入：")
    prompt = input()
    if prompt == "`":
        state = 1
    else:
        response = generate(prompt)
        print(response)
