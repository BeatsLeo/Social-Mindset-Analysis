// Determine if version is greater than all the versions possible in the range.
const outside = require('semver/ranges/outside')
const gtr = (version, range, options) => outside(version, range, '>', options)
module.exports = gtr
