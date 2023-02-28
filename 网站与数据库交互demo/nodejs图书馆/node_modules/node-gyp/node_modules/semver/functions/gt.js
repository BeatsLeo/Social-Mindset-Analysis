const compare = require('semver/functions/compare')
const gt = (a, b, loose) => compare(a, b, loose) > 0
module.exports = gt
