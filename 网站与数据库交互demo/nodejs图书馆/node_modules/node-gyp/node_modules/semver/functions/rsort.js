const compareBuild = require('semver/functions/compare-build')
const rsort = (list, loose) => list.sort((a, b) => compareBuild(b, a, loose))
module.exports = rsort
