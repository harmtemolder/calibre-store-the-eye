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
1. Note that on the next run, you might have to wait a couple of minutes until an index is built

Alternatively, run this in your terminal, pointing to the downloaded ZIP file:

```shell
calibre-customize -a "The Eye.zip"
```

## Setup

* On the first run after installing the plugin will create a local index of The Eye.
* Use the “Update Index” button in the plugin's preferences (“Preferences” > “Plugins” > select “The Eye” > “Customize plugin”) to update that local index, for example if you've been getting 404 errors when trying to download books.
* In those plugin preferences you'll also find options to restrict results to a specific file format (e.g. “epub, mobi”).

## Testing & development

While working on any of the scripts, run this from within this repository to shutdown calibre, update the plugin and restart in debug mode:

```shell
calibre-debug -s && calibre-customize -b . && calibre-debug -g
```

Or, when you're one step further, install the plugin as a user would and restart in debug mode:

```shell
calibre-debug -s && make && calibre-customize -a "The Eye.zip" && calibre-debug -g
```

## Build a release

```shell
make
```
