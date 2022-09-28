import tablemark from "tablemark" ;
import authors_h_index from "./authors_with_h_index.json" assert {type: 'json'};
import  fs from 'fs';

const authors_json = [];

authors_h_index.map((author) => 
{
  let author_h =
  {
    "profile_name" : `${author.profile_name}`,
    "profile_affiliations" : `${author.profile_affiliations}`,
    "profile_interests" : `${author.profile_interests}`,
    "h_index" : `${author.h_index}`,
  }
  authors_json.push(author_h);
})

const sorted = Object.entries(authors_json).sort(
  ([,a],[,b]) =>
  {
    return parseInt(a['h_index'])-parseInt(b['h_index']) ;
  } 
).reverse()

const res = [];
let i = 0 ;
sorted.map((author) => 
{
  author[1]['rank'] = i.toString();
  res.push(author[1]);
  i++ ;
})

const final_res = [];
res.map((author) => 
{
  let author_h =
  {
    "rank" : `${parseInt(author.rank)+1}`,
    "profile_name" : `${author.profile_name}`,
    "profile_affiliations" : `${author.profile_affiliations}`,
    "profile_interests" : `${author.profile_interests}`,
    "h_index" : `${author.h_index}`
  }
  final_res.push(author_h)
})


const table = tablemark(final_res,{ wrapWidth: 20 });
  
fs.writeFile('table.txt', table, (err) => {
    if (err) throw err;
})

