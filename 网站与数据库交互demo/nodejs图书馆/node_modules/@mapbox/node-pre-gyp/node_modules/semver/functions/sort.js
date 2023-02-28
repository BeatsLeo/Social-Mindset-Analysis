const compareBuild = require('semver/functions/compare-build')
const sort = (list, loose) => list.sort((a, b) => compareBuild(a, b, loose))
module.exports = sort
