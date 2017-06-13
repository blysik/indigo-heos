# indigo-heos

This is a plugin for the [Indigo](http://www.indigodomo.com/) smart home server that integrates the Denon Heos series
speakers.

### Requirements

1. [Indigo 7](http://www.indigodomo.com/) or later
2. Denon Heos speaker (needs to be accessible via network from the box hosting your Indigo server)

### Installing

1. Download latest release [here](https://github.com/blysik/indigo-heos/releases).
2. Follow [standard plugin installation process](http://wiki.indigodomo.com/doku.php?id=indigo_7_documentation:getting_started#installing_plugins_configuring_plugin_settings_permanently_removing_plugins)

## Usage

Add a Heos device.  Your speakers should be auto-detected, and you can add from the drop down.  Then there are Heos device
specific actions available.

## Versioning

We *will* use [SemVer](http://semver.org/) for versioning, once we get to a feature set that I consider a 1.0.0 release. For the versions available, see the [tags on this repository](https://github.com/blysik/indigo-heos/tags).

## Authors

* **Bruce Lysik** - *Initial work* - [blysik](https://github.com/blysik)

See also the list of [contributors](https://github.com/blysik/indigo-heos/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

This project uses a modified version of this Denon Heos library: https://github.com/easink/heos which doesn't have a
license listed.

## Acknowledgments

* Thanks to https://github.com/IndigoDomotics/indigo-yamaharx for structure.  This is my first python project and Indigo
plugin, and I copied a lot from indigo-yamaharx.
