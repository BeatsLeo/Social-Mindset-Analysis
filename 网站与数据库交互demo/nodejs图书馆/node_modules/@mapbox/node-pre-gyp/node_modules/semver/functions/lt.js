const compare = require('semver/functions/compare')
const lt = (a, b, loose) => compare(a, b, loose) < 0
module.exports = lt
