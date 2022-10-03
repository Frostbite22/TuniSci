import tablemark from "tablemark" ;
import authors_h_index from "./authors_with_h_index_2.json" assert {type: 'json'};
import  fs from 'fs';

const authors_json = [];

authors_h_index.map((author) => 
{
  let author_h =
  {
    "profile_name" : `${author.profile_name}`,
    "profile_affiliations" : `${author.profile_affiliations}`,
    "profile_interests" : `${author.profile_interests}`,
    "hindex" : `${author.hindex}`,
    "i10index" : `${author.i10index}`
  }
  authors_json.push(author_h);
})

const sorted = Object.entries(authors_json).sort(
  ([,a],[,b]) =>
  {
    if (Math.abs(parseInt(a['hindex'])-parseInt(b['hindex'])) > 0)
    {
      return parseInt(a['hindex'])-parseInt(b['hindex']) ;
    }
    else 
    {
      return parseInt(a['i10index'])-parseInt(b['i10index'])
    }
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
let sum = 0 ; 
res.map((author) => 
{
  sum += isNaN(parseInt(author.hindex))? 0 :parseInt(author.hindex) ; 
  let author_h =
  {
    "rank" : `${parseInt(author.rank)+1}`,
    "profile_name" : `${author.profile_name}`,
    "profile_affiliations" : `${author.profile_affiliations}`,
    "profile_interests" : `${author.profile_interests}`,
    "hindex" : `${author.hindex}`,
    "i10index" : `${author.i10index}`

  }
  final_res.push(author_h)
})


console.log(sum/final_res.length);
const table = tablemark(final_res.splice(0,1000),{ wrapWidth: 25 ,wrapWithGutters: true});
  
fs.writeFile('table.txt', table, (err) => {
    if (err) throw err;
})

