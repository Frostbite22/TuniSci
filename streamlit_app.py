import streamlit as st
import pandas as pd
import json

# Load authors data
with open("authors_with_h_index_2.json", "r") as file:
    authors_h_index = json.load(file)

# Process data
authors_json = [
    {
        "profile_name": author["profile_name"],
        "profile_affiliations": author["profile_affiliations"],
        "profile_interests": author["profile_interests"],
        "hindex": author["hindex"],
        "i10index": author["i10index"]
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
