import streamlit as st
import pandas as pd
import json

# Load authors data
with open("authors_with_h_index_2.json", "r") as file:
    authors_h_index = json.load(file)

# Process data
authors_json = [
    {
        "profile_name": author.get("profile_name", "N/A"),
        "profile_affiliations": author.get("profile_affiliations", "N/A"),
        "profile_interests": author.get("profile_interests", "N/A"),
        "hindex": author.get("hindex", 0),
        "i10index": author.get("i10index", 0)
    }
    for author in authors_h_index
]

sorted_authors = sorted(
    authors_json,
    key=lambda x: (int(x["hindex"]), int(x["i10index"])),
    reverse=True
)

for i, author in enumerate(sorted_authors):
    author["rank"] = i + 1

# Convert to DataFrame
df = pd.DataFrame(sorted_authors)

# Streamlit UI
st.title("Authors H-Index Table")
st.write(f"Average H-Index: {df['hindex'].astype(int).mean():.2f}")
st.dataframe(df.head(1000))
