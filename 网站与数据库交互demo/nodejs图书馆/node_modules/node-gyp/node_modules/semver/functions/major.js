const SemVer = require('semver/classes/semver')
const major = (a, loose) => new SemVer(a, loose).major
module.exports = major
