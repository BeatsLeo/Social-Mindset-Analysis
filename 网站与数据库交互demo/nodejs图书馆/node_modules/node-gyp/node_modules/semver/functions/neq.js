const compare = require('semver/functions/compare')
const neq = (a, b, loose) => compare(a, b, loose) !== 0
module.exports = neq
