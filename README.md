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
calibre-customize -a "The Eye.zip"
```

## Setup

* Note that this plugin searches a local index of The Eye. Before being able to search, you’ll have to click the “Update Index” button in the plugin's preferences (“Preferences” > “Plugins” > select “The Eye” > “Customize plugin”) to create or update that local index.
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
