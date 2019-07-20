const parser = require('periodo-date-parser');

module.exports = { parse };  // entry for node

function parse(payload) {
  try {
    result = parser.parse(payload);
    result = result.in;
    if( result.year ) {
      console.log(result.year);
    } else if( result.earliestYear && result.latestYear ) {
      console.log(Math.floor((parseInt(result.earliestYear) + parseInt(result.latestYear)) / 2));
    } else return false;
 } catch(err) {
    console.log(err);
    return false;
  }
}
