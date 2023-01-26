# semantify

[![On_Push_build](https://github.com/vliz-be-opsci/semantify/actions/workflows/build.yml/badge.svg)](https://github.com/vliz-be-opsci/semantify/actions/workflows/build.yml)

`semantify` is a GitHub action that makes use of `pysembench` to semantically uplift your data.

## How to use ##

```
name: Semantic Uplifting
on:
  push:
    branches:
      - main  # Set a branch name to trigger deployment
  pull_request:
jobs:
  Semantic_Uplifting:
    runs-on: ubuntu-20.04
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
    steps:
      # Checkout this repo
      - uses: actions/checkout@v3 

      # Semantic Uplifting of files
      - name: Semantic Uplifting
        uses: vliz-be-opsci/semantify@latest
```
