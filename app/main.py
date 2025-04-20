from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request, jsonify
from flask_cors import CORS
from util.parser import extract_json_parts

tokenizer = AutoTokenizer.from_pretrained("./resources/distilgpt2-v2")
model = AutoModelForCausalLM.from_pretrained("./resources/distilgpt2-v2")
tokenizer.pad_token = tokenizer.eos_token
model.eval()

app = Flask(__name__)
CORS(app)

@app.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients", "")

    if not ingredients:
        return jsonify({"error": "Missing 'ingredients' field"}), 400

    prompt = f"Ingredients: {ingredients}\nInstructions:"
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")

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

    return jsonify(parsed_output)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)