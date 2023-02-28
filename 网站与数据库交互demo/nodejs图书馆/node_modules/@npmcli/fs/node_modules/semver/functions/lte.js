const compare = require('semver/functions/compare')
const lte = (a, b, loose) => compare(a, b, loose) <= 0
module.exports = lte
