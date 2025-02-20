import json
import re


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

def save_cleaned_json(cleaned_data):
    # Save the cleaned data back to a new JSON file
    with open("authors_with_h_index.json", "w", encoding="utf-8") as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

def json_to_flattened_text_azure_ai(json_file_path):
    # Load the large JSON document
    with open(json_file_path, "r", encoding="utf-8") as file:
        authors = json.load(file)

    # Convert the JSON to a formatted string for better chunking
    def flatten_json(json_obj, indent=0):
        """Flatten nested JSON into key-value pairs."""
        out = {}

        def recurse(t, parent_key=""):
            if isinstance(t, dict):
                for k, v in t.items():
                    recurse(v, parent_key + k + ".")
            elif isinstance(t, list):
                for i, v in enumerate(t):
                    recurse(v, parent_key + str(i) + ".")
            else:
                out[parent_key[:-1]] = t

        recurse(json_obj)
        return out
    # Flatten and join the JSON as a string
    flattened_text = [json.dumps(flatten_json(author)) for author in authors]

    return flattened_text

def json_to_flattened_text(json_file_path):
    # Load the large JSON document
    with open(json_file_path, "r", encoding="utf-8") as file:
        authors = json.load(file)

    formatted_chunks = []
    
    for author in authors:
        chunk = f"""Author: {author.get('profile_name', 'N/A')}
Profile Link: {author.get('profile_link', 'N/A')}
Research Interests: {', '.join(author.get('profile_interests', []))}
Affiliation: {author.get('profile_affiliations', 'N/A')}
Email: {author.get('profile_email', 'N/A')}
H-index: {author.get('hindex', 'N/A')}
H-index (5y): {author.get('hindex5y', 'N/A')}
i10-index: {author.get('i10index', 'N/A')}
i10-index (5y): {author.get('i10index5y', 'N/A')}
"""
        formatted_chunks.append(chunk)
    
    return formatted_chunks



def json_to_flattened_text_openai(json_file_path):
    # Load the large JSON document
    with open(json_file_path, "r", encoding="utf-8") as file:
        large_json = json.load(file)

    # Convert the JSON to a formatted string for better chunking
    def flatten_json(json_obj, indent=0):
        result = []
        for key, value in json_obj.items():
            if isinstance(value, dict):
                result.append(f"{'  ' * indent}{key}:")
                result.extend(flatten_json(value, indent + 1))
            elif isinstance(value, list):
                result.append(f"{'  ' * indent}{key}: [")
                for item in value:
                    result.append(f"{'  ' * (indent + 1)}- {json.dumps(item)}")
                result.append(f"{'  ' * indent}]")
            else:
                result.append(f"{'  ' * indent}{key}: {json.dumps(value)}")
        return result

    # Flatten and join the JSON as a string
    flattened_text = "\n".join([item for author in large_json for item in flatten_json(author)])
    return flattened_text

