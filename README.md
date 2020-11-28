# calibre store for The Eye
The Eye store plugin for calibre

## Installation
Download the latest ZIP from [the “Releases” page](https://github.com/harmtemolder/calibre-store-the-eye/releases) and follow these steps to add the plugin to calibre:

1. Open calibre
1. Open Preferences (<kbd>⌘</kbd>+<kbd>,</kbd>)
1. Open Plugins, bottom left
1. Click “Load plugin from file”, bottom right
1. Point the dialog to the downloaded ZIP file
1. Click “Apply”
1. Quit and restart calibre

Alternatively, run this in your terminal, pointing to the downloaded ZIP file:

```shell
calibre-customize -a "The Eye vX.X.X.zip"
```

Where `X.X.X` is the release you’ve downloaded.

## Setup
* Note that this plugin searches a local index of The Eye. Before being able to search, you’ll have to click the “Update Index” button in the plugin's preferences (“Preferences” > “Plugins” > select “The Eye” > “Customize plugin”) to create or update that local index.
* In those plugin preferences you'll also find options to restrict results to a specific file format (e.g. “epub, mobi”).

## Searching
* Because the index really is just a long list of URLs, there is no difference between “Title”, “Author” or “Keyword” when searching. I arbitrarily chose the first one, which means you can type anything you’re looking for in the “Title” field and ignore the other two.
* Note that searching is case-insensitive.

## Testing & development
While working on any of the scripts, run this from within this repository to shutdown calibre, update the plugin and restart in debug mode:

```shell
calibre-debug -s && calibre-customize -b . && calibre-debug -g
```

Or, when you're one step further, install the plugin as a user would and restart in debug mode:

```shell
calibre-debug -s && make && calibre-customize -a "releases/The Eye vX.X.X.zip" && calibre-debug -g
```

Where `X.X.X` is the release you’re testing.

## Build a release
```shell
make
```

## Changelog
All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.3-alpha]: 2020-11-28
### Changed
- Only update index when forced

## [0.2.2-alpha]: 2020-11-26
### Changed
- Added line breaks in the index, in case anyone wants to open it in a text editor
- Added note about how to use the search to `README.md`

## [0.2.1-alpha]: 2020-11-25
### Added
- `TODO` file

### Changed
- Fixed `gzip` writing corrupt archives
- Changelog in `README.md`
- More `debug_print`
- Reordered config window
- `make zip` now zips into `releases` folder and numbered
- `pydevd_pycharm` now handled more cleanly, with the `PYDEVD` variable

### Removed
- `if __name__ == "__main__"` sections from `main.py` and `config.py`

[Unreleased]: https://github.com/harmtemolder/calibre-store-the-eye/archive/master.zip
[0.2.1-alpha]: https://github.com/harmtemolder/calibre-store-the-eye/releases/tag/v0.2.1-alpha
[0.2.2-alpha]: https://github.com/harmtemolder/calibre-store-the-eye/releases/tag/v0.2.2-alpha
[0.2.3-alpha]: https://github.com/harmtemolder/calibre-store-the-eye/releases/tag/v0.2.3-alpha
