# A high level roadmap for TuniSci 

## Improve the RAG capabilities :
Currently, we are relying on a strictly defined dataset to generate the responses for the users. 
This dataset is somehow limited, some researchers does not have a google scholar profile, some we didn't extract their information etc..
For that purpose, whenever the RAG fails to find appropriate data, we will invoke a search so that we can get the right data. 

## Make the abstraction classes more flexible
While this projects gets a JSON file input to be processed. It would be better if the abstraction classes get any type of input such as : 
1.  Documents
2.  CSV files

## Scrap better data 
The current data are scrapped in 2022, with some wrong entries in the scrapped data. The data has certainly evoled today in 2025. It would be better if we do another round of data scrapping and update the ranking. 

