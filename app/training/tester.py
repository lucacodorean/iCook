from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
import ast

def extract_json_parts(generated_text):
    result = {
        "ingredients": [],
        "instructions": [],
        "link": None,
        "source": None,
    }

    title_match = re.search(r"Title:\s*(.+)", generated_text)
    if title_match:
        result["title"] = title_match.group(1).strip()

    ingredients_match = re.search(r"Ingredients:\s*(.+?)\n", generated_text)
    if ingredients_match:
        raw_ingredients = ingredients_match.group(1).strip()
        result["ingredients"] = [i.strip() for i in raw_ingredients.split(",") if i.strip()]

    instructions_match = re.search(r"Instructions:\s*(.+?)\n(?:Link:|Source:|NER:|$)", generated_text, re.DOTALL)
    if instructions_match:
        raw_instructions = instructions_match.group(1).strip()
        try:
            parsed_list = ast.literal_eval(raw_instructions)
            if isinstance(parsed_list, list):
                result["instructions"] = [i.strip() for i in parsed_list]
            else:
                raise ValueError
        except:
            sentences = re.split(r'\.\s*|\n+', raw_instructions)
            cleaned = [s.strip() + '.' for s in sentences if s.strip()]
            result["instructions"] = cleaned

    link_match = re.search(r"Link:\s*(\S+)", generated_text)
    if link_match:
        result["link"] = link_match.group(1).strip()

    source_match = re.search(r"Source:\s*(.+)", generated_text)
    if source_match:
        result["source"] = source_match.group(1).strip()

    return result


tokenizer = AutoTokenizer.from_pretrained("../resources/distilgpt2-v2")
model = AutoModelForCausalLM.from_pretrained("../resources/distilgpt2-v2")
tokenizer.pad_token = tokenizer.eos_token 

prompt = "Ingredients: Eggs, milk, sugar, flour\nInstructions"
inputs = tokenizer(prompt, return_tensors="pt", padding=True)

input_ids = inputs["input_ids"]
attention_mask = inputs["attention_mask"]

outputs = model.generate(
    input_ids=input_ids,
    attention_mask=attention_mask,
    max_new_tokens=100,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    pad_token_id=tokenizer.eos_token_id
)


decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
parsed_output = extract_json_parts(decoded)
print(parsed_output)
