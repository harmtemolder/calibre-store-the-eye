# Calibre store for The Eye

A The Eye store plugin for Calibre

## Installation

Download the latest ZIP from here and follow these steps to add the plugin to Calibre:

1. Open Calibre, obviously
1.

## Testing & development

While working on any of the scripts, run this to shutdown Calibre, update the plugin and restart in debug mode:

```shell
calibre-debug -s && calibre-customize -b . && calibre-debug -g
```

## Build a release

Run this to zip all PY files together:

```shell
./zip.sh
```
