# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.0.6]
### Fixed
- Added logic to detect 'command under process' message
- Added Heos icon for Indigo Plugin Store
- Adding logic to guard against keys not being present in media info

## [0.0.5]
### Fixed
- Updated CHANGELOG.md formatting
- Added 'import traceback' to plugin.py
- Account for an unknown play status from a device
- Added socket timeout handling for heos.py lib

## [0.0.4]
### Fixed
- Fix "TypeError: refresh_speaker_list() takes exactly 1 argument (4 given)"
- Fix "TypeError: Expecting an object of type list; got an object of type NoneType instead"

## [0.0.3]
### Fixed
- "Play Input From Other Speaker": was incorrectly using inputs of playing device,
rather than other speaker

## [0.0.2]
### Changed
- "Play Input From Other Speaker" now generates a list of inputs to select,
rather than using a text input field

### Fixed
- README.md: url for tags list

## 0.0.1 - 2017-06-12
### Added
- Initial version

[Unreleased]: https://github.com/blysik/indigo-heos/compare/0.0.6...HEAD
[0.0.6]: https://github.com/blysik/indigo-heos/compare/0.0.5...0.0.6
[0.0.5]: https://github.com/blysik/indigo-heos/compare/0.0.4...0.0.5
[0.0.4]: https://github.com/blysik/indigo-heos/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/blysik/indigo-heos/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/blysik/indigo-heos/compare/0.0.1...0.0.2
