import tablemark from "tablemark";
import authors_h_index from "./authors_with_h_index_new_11.json" with { type: "json" };
import fs from 'fs';

const authors_json = [];

authors_h_index.map((author) => {
  let author_h = {
    "profile_name": `${author.profile_name}`,
    "profile_affiliations": `${author.profile_affiliations}`,
    "profile_interests": `${author.profile_interests}`,
    "hindex": `${author.hindex}`,
    "i10index": `${author.i10index}`
  }
  authors_json.push(author_h);
});

// Fixing the sorting logic - comparing b to a for descending order
const sorted = Object.entries(authors_json).sort(
  ([, a], [, b]) => {
    // First compare h-index
    const hIndexA = parseInt(a['hindex']) || 0;
    const hIndexB = parseInt(b['hindex']) || 0;
    
    if (hIndexA !== hIndexB) {
      return hIndexB - hIndexA; // Sort by h-index descending
    } else {
      // If h-indices are equal, compare i10-index
      const i10A = parseInt(a['i10index']) || 0;
      const i10B = parseInt(b['i10index']) || 0;
      return i10B - i10A; // Sort by i10-index descending
    }
  }
);

// Add ranking
const res = [];
let i = 0;
sorted.map((author) => {
  author[1]['rank'] = i.toString();
  res.push(author[1]);
  i++;
});

// Build final result with calculated rank
const final_res = [];
let sum = 0;
res.map((author) => {
  sum += isNaN(parseInt(author.hindex)) ? 0 : parseInt(author.hindex);
  let author_h = {
    "rank": `${parseInt(author.rank) + 1}`,
    "profile_name": `${author.profile_name}`,
    "profile_affiliations": `${author.profile_affiliations}`,
    "profile_interests": `${author.profile_interests}`,
    "hindex": `${author.hindex}`,
    "i10index": `${author.i10index}`
  }
  final_res.push(author_h);
});

// Calculate and display average h-index
console.log(`Average h-index: ${(sum / final_res.length).toFixed(2)}`);

// Generate table and write to file
const table = tablemark(final_res.splice(0, 1000), { wrapWidth: 25, wrapWithGutters: true });

fs.writeFile('table.txt', table, (err) => {
  if (err) throw err;
  console.log('Table has been written to table.txt');
});