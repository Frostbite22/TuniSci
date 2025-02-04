import json
import re

# Load the JSON file
with open("authors_with_h_index_2.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Function to clean non-ASCII Unicode characters (removes Chinese characters, control chars, etc.)
def clean_unicode(text):
    if isinstance(text, str):
        # Keep only printable ASCII characters (letters, numbers, punctuation, and basic symbols)
        text = re.sub(r'[^\x20-\x7E]', '', text)
    return text

# Recursively clean all values in the JSON
def clean_json(obj):
    if isinstance(obj, dict):
        return {key: clean_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [clean_json(item) for item in obj]
    else:
        return clean_unicode(obj)

# Clean the entire JSON dataset
cleaned_data = clean_json(data)

# Save the cleaned data back to a new JSON file
with open("authors_with_h_index.json", "w", encoding="utf-8") as file:
    json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

print("JSON data cleaned and saved!")
