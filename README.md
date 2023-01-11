# ROCrate_Semantic_Uplifting_By_PYSUBYT

[![On_Push_build](https://github.com/vliz-be-opsci/ROCrate_Semantic_Uplifting_By_PYSUBYT/actions/workflows/build.yml/badge.svg)](https://github.com/vliz-be-opsci/ROCrate_Semantic_Uplifting_By_PYSUBYT/actions/workflows/build.yml)

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

      # Build the preview.html file from the rocrate.json
      #- name: Build Preview HTML
      #  uses: vliz-be-opsci/rocrate-to-pages@latest #vliz-be-opsci/new_rocrate_to_pages@latest

      # New html to pages 
      - name: Semantic Uplifting
        uses: vliz-be-opsci/ROCrate_Semantic_Uplifting_By_PYSUBYT@latest
```
