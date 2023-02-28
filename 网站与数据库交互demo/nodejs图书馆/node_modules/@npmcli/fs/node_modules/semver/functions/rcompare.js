const compare = require('semver/functions/compare')
const rcompare = (a, b, loose) => compare(b, a, loose)
module.exports = rcompare
