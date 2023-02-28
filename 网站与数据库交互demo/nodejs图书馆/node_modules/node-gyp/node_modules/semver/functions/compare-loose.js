const compare = require('semver/functions/compare')
const compareLoose = (a, b) => compare(a, b, true)
module.exports = compareLoose
