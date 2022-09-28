import tablemark from "tablemark" ;
import authors_h_index from "./authors_with_h_index.json" assert {type: 'json'};

const authors_json = [];

authors_h_index.map((author) => 
{
  let author_h =
  {
    "profile_name" : `${author.profile_name}`,
    "profile_affiliations" : `${author.profile_affiliations}`,
    "profile_interests" : `${author.profile_interests}`,
    "h_index" : `${author.h_index}`
  }
  authors_json.push(author_h);

})


console.log(tablemark(authors_json,{ wrapWidth: 20 }),
);
