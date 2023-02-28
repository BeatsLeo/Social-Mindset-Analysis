const SemVer = require('semver/classes/semver')
const patch = (a, loose) => new SemVer(a, loose).patch
module.exports = patch
