import re

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
            import ast
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
