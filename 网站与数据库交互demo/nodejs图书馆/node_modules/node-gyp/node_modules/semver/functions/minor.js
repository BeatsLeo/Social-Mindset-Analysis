const SemVer = require('semver/classes/semver')
const minor = (a, loose) => new SemVer(a, loose).minor
module.exports = minor
