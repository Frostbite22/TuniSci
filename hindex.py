from scholarly import scholarly

# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_author('Adel Trabelsi')
author = next(search_query).fill(sections=['indices'])
print(author)

